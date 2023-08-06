
import threading
import time
import random

s_running = True


class QThreadProducer(threading.Thread):

    def __init__(self, name, queue, lock):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.lock = lock
        self.running = True

    def run(self) -> None:
        while True:
            if self.queue.full():
                print(f"生产者{self.name}队列已满，暂停生产")
                time.sleep(1)
            else:
                num = random.randint(0, 100)
                self.queue.put(num)
                print(f"生产者 {self.name} ,生产了 {num}")
                time.sleep(1)

            with self.lock:
                if not self.running:
                    print(f"生产者{self.running} running:{self.running}")
                    break
                else:
                    print(f"生产者{self.running} running:{self.running}")
                # if not s_running:
                #     print("QThreadProducer-run", s_running)
                #     break
                # else:
                #     print("QThreadProducer-run", s_running)

        print(f"{self.name} 线程退出")

    def stop(self):
        with self.lock:
            self.running = False


class QThreadConsumer(threading.Thread):

    def __init__(self, name, queue, lock):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.lock = lock
        self.running = True

    def run(self) -> None:
        while True:
            if self.queue.empty():
                print(f"消费者{self.name}队列已空， 暂停消费")
                time.sleep(1.5)
            else:
                v = self.queue.get()
                print(f"消费者 = {self.name},消费了 {v}")
                self.queue.task_done()
                time.sleep(1.5)

            with self.lock:
                if not self.running:
                    print(f"消费者{self.name} running:{self.running}")
                    break
                else:
                    print(f"消费者{self.name} running:{self.running}")
                # if not s_running:
                #     print("QThreadConsumer-run", self.running)
                #     break
                # else:
                #      print("QThreadConsumer-run", self.running)

        print(f'{self.name}消费者线程退出')

    def stop(self):
        with self.lock:
            self.running = False

