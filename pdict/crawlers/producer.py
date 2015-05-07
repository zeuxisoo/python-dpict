from multiprocessing import Queue, cpu_count
from .consumer import AlphabetConsumer

class AlphabetListProducer(object):

    def __init__(self, logger, alphabet_list):
        self.logger         = logger
        self.alphabet_queue = Queue()
        self.parse_queue    = Queue()
        self.alphabet_list  = alphabet_list

    def start(self):
        # Consumer pool
        consumers = []
        for i in xrange(0, cpu_count()):
            consumer = AlphabetConsumer(self.logger, self.alphabet_queue, self.parse_queue)
            consumer.start()

            consumers.append(consumer)

        # Add each alphabet array into queue
        for alphabet in self.alphabet_list:
            self.alphabet_queue.put(alphabet)

        # Join the consumer
        try:
            for consumer in consumers:
                consumer.join()
        except KeyboardInterrupt:
            print("ByeBye")
