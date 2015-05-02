from multiprocessing import Process

class AlphabetConsumer(Process):

    def __init__(self, logger, queue):
        super(AlphabetConsumer, self).__init__()

        self.logger = logger
        self.queue  = queue

    def run(self):
        while True:
            task = self.queue.get()

            if isinstance(task, str) and task == 'quit':
                break;

            self.logger.info("AlphabetConsumer Task: {0}".format(task))

        self.logger.info('AlphabetConsumer Action: Exit')
