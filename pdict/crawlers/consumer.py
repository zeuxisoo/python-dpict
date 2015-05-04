from multiprocessing import Process, Lock
from urllib import quote_plus
from urllib2 import urlopen
from mimetypes import guess_type
from time import sleep
from pyquery import PyQuery as pq
from ..models import Word

class AlphabetConsumer(Process):

    def __init__(self, logger, alphabet_queue, parse_queue):
        super(AlphabetConsumer, self).__init__()

        self.lock            = Lock()
        self.logger          = logger
        self.alphabet_queue  = alphabet_queue
        self.parse_queue     = parse_queue

    def format_log(self, message):
        return "[{0}] {1}".format(self.name, message)

    def fetch_alphabet(self, alphabet):
        self.lock.acquire()

        exists_count = Word.select(Word.id).where(Word.moccasin == alphabet).count()

        if exists_count > 0:
            return
        else:
            document  = pq(
                url="http://www.onlinedict.com/servlet/MobiDictLookup14?WoRd={0}&example=true&phrase=true&from=prev".format(quote_plus(alphabet)),
                headers={
                    'user-agent'     : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
                    'X-Forwarded-For': '::ffff:24.127.96.129'
                }
            )

            table         = document("table tr:nth-child(2) td")
            moccasin      = table.find("tr[bgcolor=moccasin] td font b").text()
            beige         = table.find("tr[bgcolor=beige] td font b").text()
            previous_word = table.find("tr:nth-last-child(5) td a").html()
            next_word     = table.find("tr:nth-last-child(4) td a").html()

            if next_word:
                self.logger.info(self.format_log("next {0} -> {1}".format(alphabet, next_word)))

                Word.create(
                    moccasin=moccasin,
                    beige=beige,
                    previous_word=previous_word,
                    next_word=next_word,
                    content=None
                )

                self.alphabet_queue.put(next_word)
                self.parse_queue.put(document)
            else:
                self.logger.info(self.format_log("not found next in {0}".format(alphabet)))

        self.lock.release()

        sleep(3)

    def run(self):
        while True:
            alphabet = self.alphabet_queue.get()

            if isinstance(alphabet, str) and alphabet == 'quit':
                break;

            self.logger.info(self.format_log("alphabet {0}".format(alphabet)))
            self.fetch_alphabet(alphabet)

            sleep(1)

        self.logger.info(self.format_log("exit"))
