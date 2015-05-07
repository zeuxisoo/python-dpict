import signal
from multiprocessing import Process, Lock
from urllib import quote_plus
from urllib2 import urlopen
from mimetypes import guess_type
from time import sleep
from random import choice, randint
from socket import inet_ntoa
from struct import pack
from pyquery import PyQuery as pq
from ..models import Word

class AlphabetConsumer(Process):

    def __init__(self, logger, alphabet_queue, parse_queue):
        super(AlphabetConsumer, self).__init__()

        signal.signal(signal.SIGTERM, self.handler_sigterm)
        signal.signal(signal.SIGQUIT, self.handler_sigquit)

        self.is_stop         = False
        self.lock            = Lock()
        self.logger          = logger
        self.alphabet_queue  = alphabet_queue
        self.parse_queue     = parse_queue

    def handler_sigterm(self):
        self.is_stop = True

    def handler_sigquit(self):
        self.is_stop = True

    def log_info(self, message):
        self.logger.info("[{0}] {1}".format(self.name, message))

    def log_fetch_info(self, alphabet, message):
        self.log_info("FetchAlphabet ({0}) => {1}".format(alphabet, message))

    def fetch_alphabet(self, alphabet):
        self.lock.acquire()

        try:
            self.log_fetch_info(alphabet, "getting web page")

            user_agents = (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
                'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko',
                'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
            )

            document  = pq(
                url="http://www.onlinedict.com/servlet/MobiDictLookup14?WoRd={0}&example=true&phrase=true&from=prev".format(quote_plus(alphabet)),
                headers={
                    'user-agent'     : choice(user_agents),
                    'X-Forwarded-For': inet_ntoa(pack('>I', randint(1, 0xffffffff))),
                    'Referer'        : "http://www.onlinedict.com/servlet/MobiDictLookup14"
                },
                timeout=5
            )

            # Find base information
            self.log_fetch_info(alphabet, "finding base information")

            table         = document("table tr:nth-child(2) td")
            moccasin      = table.find("tr[bgcolor=moccasin] td font b").text()
            beige         = table.find("tr[bgcolor=beige] td font b").text()
            previous_word = table.find("tr:nth-last-child(5) td a").html()
            next_word     = table.find("tr:nth-last-child(4) td a").html()

            # Show next word to log
            self.log_fetch_info(alphabet, "next word is {0} -> {1}".format(alphabet, next_word))

            # Check word is or not exists in database
            exists_count  = Word.select(Word.id).where(Word.moccasin == alphabet).count()

            if exists_count > 0:
                self.log_fetch_info(alphabet, "already exists: {0}".format(alphabet))

            # Add word to database if it is not eixsts
            if exists_count <= 0 and next_word:
                Word.create(
                    moccasin=moccasin,
                    beige=beige,
                    previous_word=previous_word,
                    next_word=next_word,
                    content=None
                )

                self.parse_queue.put(document.html())

            # Handle next word status
            # If not next word, show message to log and add back to queue
            # If has next word, add it to alphabet queue
            if next_word is None:
                self.log_fetch_info(alphabet, "not found next word in {0}, added back to queue".format(alphabet))

                self.alphabet_queue.put(alphabet)

                # Save html
                # with open("./{0}.html".format(alphabet), 'w+') as f:
                #     f.write(document.html().encode("utf-8"))
                #     f.close()
            else:
                self.alphabet_queue.put(next_word)

            # Check the first char is or not equals between current word and next word
            # If not: push quit message to current queue, ask worker exists
            if isinstance(next_word, str) and alphabet[0].lower() != next_word[0].lower():
                self.log_fetch_info(alphabet, "first char different (alphabet: {0}, next: {1})".format(alphabet.lower(), next_word.lower()))
                self.alphabet_queue.put("quit")

            self.log_fetch_info(alphabet, "zZzz ...")
        except KeyboardInterrupt:
            pass
        finally:
            self.lock.release()
            sleep(30)

    def run(self):
        try:
            while not self.is_stop:
                alphabet = self.alphabet_queue.get()

                if isinstance(alphabet, str) and alphabet == 'quit':
                    break;

                self.fetch_alphabet(alphabet)

                sleep(1)

            self.log_info("exit")
        except KeyboardInterrupt:
            pass
