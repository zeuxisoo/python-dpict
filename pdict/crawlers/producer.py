from multiprocessing import Queue
from .consumer import AlphabetConsumer

class AlphabetGroupProducer(object):

    def __init__(self, logger, alphabet_group):
        self.logger         = logger
        self.alphabet_queue = Queue()
        self.alphabet_group = alphabet_group

    def start(self):
        # Consumer pool
        consumers = []
        for i in xrange(0, len(self.alphabet_group)):
            consumer = AlphabetConsumer(self.logger, self.alphabet_queue)
            consumer.start()

            consumers.append(consumer)

        # Add each alphabet array into queue
        for alphabet in self.alphabet_group:
            self.alphabet_queue.put(alphabet)

        # Add quit keyword for exit consumer
        for consumer in consumers:
            self.alphabet_queue.put("quit")

        # Join the consumer
        for consumer in consumers:
            consumer.join()
