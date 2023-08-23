import queue
import threading
import time

class QueueTest(object):
    MAX_THREAD_NUM = 3
    MAX_QUEUE_NUM = 10

    def __init__(self):
        self.exit_flag = False
        self.lock = threading.Lock()
        self.queue = queue.Queue(QueueTest.MAX_QUEUE_NUM)
        self.lifo_queue = queue.LifoQueue(QueueTest.MAX_QUEUE_NUM)
        self.priority_queue = queue.PriorityQueue(QueueTest.MAX_QUEUE_NUM)

    def work(self):

        while True:
            try:
                item = self.queue.get()
                print(f"---work---item:{item}")
                self.queue.task_done()
            except self.queue.empty():
                print(f"queue empty")

            time.sleep(2)

            with self.lock:
                if self.exit_flag:
                    break

    def lifo_work(self):

        while True:
            try:
                item = self.lifo_queue.get()
                print(f"---lifo_work---item:{item}")
                self.lifo_queue.task_done()
            except self.lifo_queue.empty():
                print(f"lifo_queue empty")

            time.sleep(2)

            with self.lock:
                if self.exit_flag:
                    break

    def priority_work(self):

        while True:
            try:
                item = self.priority_queue.get()
                print(f"---priority_queue---item:{item}")
                self.priority_queue.task_done()
            except self.priority_queue.empty():
                print(f"priority_queue empty")

            time.sleep(2)

            with self.lock:
                if self.exit_flag:
                    break


    def start(self):

        threads = []

        print(f"---queue---")
        # 先入先出
        for i in range(QueueTest.MAX_THREAD_NUM):
            t = threading.Thread(target=self.work)
            threads.append(t)
            t.start()

        for i in range(QueueTest.MAX_QUEUE_NUM):
            self.queue.put(i)

        self.queue.join()

        with self.lock:
            self.exit_flag = True

        for i in range(QueueTest.MAX_THREAD_NUM):
            threads[i].join(timeout=10)

        threads.clear()

        print(f"---lifo_queue---")
        # 后入先出
        self.exit_flag = False

        for i in range(QueueTest.MAX_THREAD_NUM):
            t = threading.Thread(target=self.lifo_work)
            threads.append(t)
            t.start()

        for i in range(QueueTest.MAX_QUEUE_NUM):
            self.lifo_queue.put(i)

        self.lifo_queue.join()

        with self.lock:
            self.exit_flag = True

        for i in range(QueueTest.MAX_THREAD_NUM):
            threads[i].join(timeout=10)

        threads.clear()

        print(f"---priority_queue---")

        self.exit_flag = False

        for i in range(QueueTest.MAX_THREAD_NUM):
            t = threading.Thread(target=self.priority_work)
            threads.append(t)
            t.start()

        for i in range(QueueTest.MAX_QUEUE_NUM):
            self.priority_queue.put((QueueTest.MAX_QUEUE_NUM - i, "hello priority_queue" + str(QueueTest.MAX_QUEUE_NUM - i)))

        self.priority_queue.join()

        with self.lock:
            self.exit_flag = True

        for i in range(QueueTest.MAX_THREAD_NUM):
            threads[i].join(timeout=10)

        threads.clear()

        print(f"---all finish---")

    def make_queue_test(self, threads, queue, target):

        for i in range(QueueTest.MAX_THREAD_NUM):
            t = threading.Thread(target=target)
            threads.append(t)
            t.start()

        for i in range(20):
            queue.put(i)

        queue.join()

        with self.lock:
            self.exit_flag = True

        for i in range(QueueTest.MAX_THREAD_NUM):
            threads[i].join(timeout=10)

        threads.clear()