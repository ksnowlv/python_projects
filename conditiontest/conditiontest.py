import threading


class ConditionTest(object):

    def __init__(self):
        self.ready = False
        self.data = None
        self.condition = threading.Condition()
        self.producer_thread = threading.Thread(target=self.producer, args=("Hello, I am comming!!!", ))
        self.consumer_thread = threading.Thread(target=self.consumer)

    def producer(self, data):
        print(f"---producer--- start")
        with self.condition:
            while self.ready:
                self.condition.wait()

            self.data = data
            print(f"---producer data---{self.data} ")
            self.ready = True
            self.condition.notify()

        print(f"---producer--- finish")

    def consumer(self):
        print(f"---consumer--- start")
        with self.condition:
            while not self.ready:
                self.condition.wait()
            data = self.data
            print(f"consumer received data:{data}")
            self.ready = False
            self.condition.notify()
        print(f"---consumer--- finish")

    def start(self):
        self.producer_thread.start()
        self.consumer_thread.start()

        self.producer_thread.join()
        self.consumer_thread.join()
