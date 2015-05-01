from multiprocessing import Process

class AlphabetConsumer(Process):

    def __init__(self, queue):
        super(AlphabetConsumer, self).__init__()

        self.queue = queue

    def run(self):
        while True:
            task = self.queue.get()

            if isinstance(task, str) and task == 'quit':
                break;

            print task

        print 'AlphabetConsumer Exit'
