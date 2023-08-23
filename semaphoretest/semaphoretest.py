import threading
import time


class SemaphoreTest(object):

    def __init__(self):
        self.semaphore = threading.Semaphore(1)
        self.lock = threading.Lock()
        self.exit_flag = False
        self.producer_thread = threading.Thread(target=self.producer)
        self.consumer_thread = threading.Thread(target=self.consumer)

    def producer(self):

        while True:
            self.semaphore.acquire()
            try:
                print(f"producer is working!!!")
            except Exception as e:
                print(f"producer发生异常:{e}")
            finally:
                self.semaphore.release()

            time.sleep(1)

            with self.lock:
                if self.exit_flag:
                    break

    def consumer(self):

        while True:
            self.semaphore.acquire()
            try:
                print(f"consumer is working!!!")
            except Exception as e:
                print(f"consumer发生异常:{e}")
            finally:
                self.semaphore.release()

            time.sleep(1)

            with self.lock:
                if self.exit_flag:
                    break

    def start_thread(self):

        self.producer_thread.start()
        self.consumer_thread.start()

    def stop_thread(self):

        time.sleep(5)
        with self.lock:
            self.exit_flag = True

        self.producer_thread.join()
        self.consumer_thread.join()
