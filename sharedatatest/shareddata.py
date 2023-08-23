import threading


class SharedData(object):
    _count = 0

    def __init__(self):
        # self.lock = threading.RLock()
        self.lock = threading.Lock()
        self.threads = []

    def count_increment(self):
        with self.lock:
            for i in range(5):
                SharedData._count += i
            print(f"count:{SharedData._count}")

    def start(self):

        for i in range(5):
            self.threads.append(threading.Thread(target=self.count_increment))
            self.threads[i].start()

        for i in range(5):
            self.threads[i].join()
