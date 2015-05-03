from multiprocessing import Process

class AlphabetConsumer(Process):

    def __init__(self, logger, queue):
        super(AlphabetConsumer, self).__init__()

        self.logger = logger
        self.queue  = queue

    def format_log(self, message):
        return "[{0}] {1}".format(self.name, message)

    def run(self):
        while True:
            task = self.queue.get()

            if isinstance(task, str) and task == 'quit':
                break;

            self.logger.info(self.format_log("task {0}".format(task)))

        self.logger.info(self.format_log("exit"))
