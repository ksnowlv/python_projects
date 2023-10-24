from multiprocessing import Process, Queue, Value, Array, Semaphore, Pool, Pipe
import multiprocessing
import time
import os


class ProcessTest(object):

    def __init__(self):
        self.queue = Queue(maxsize=5)
        self.shared_value = Value('i', 0)
        self.shared_array = Array('i', [1, 2, 3, 4, 5])
        self.semaphore = Semaphore(1)

    def work_with_pipe(self, connection):

        while True:
            data = connection.recv()
            print(f"child_process recv {data}")
            if data == "close":
                break
            elif type(data) in [int, float]:
                result = data * 3
                connection.send(result)

        try:
            connection.close()
        except Exception as e:
            print(f"error = {e}")


    def start_with_pipe(self):
        parent_connection, child_connection = Pipe()
        child_process = Process(target=self.work_with_pipe, args=(child_connection,))
        child_process.start()

        for i in range(1, 5):
            parent_connection.send(i)
            res = parent_connection.recv()
            print(f"parent_connection recv {res}")

        parent_connection.send("close")

        child_process.join()
        print(f"process finish")

    def work_with_queue_produce(self):

        for i in range(5):
            self.queue.put(i)
            time.sleep(1)

        self.queue.put(None)

    def work_with_queue_consume(self):

        while True:
            try:
                item = self.queue.get()
                if item is None:
                    print(f"---consume--- finish")
                    break
                print(f"---consume--- item:{item}")
            except Exception as e:
                print(f"---consume--- error:{e}")

    def start_with_queue(self):
        producer = Process(target=self.work_with_queue_produce)
        consumer = Process(target=self.work_with_queue_consume)
        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

    def work_with_shared_memory1(self):
        self.shared_value.value += 1

        for i in range(len(self.shared_array)):
            self.shared_array[i] += 1

        print(
            f"---process_data_shared_memory1---"
            f"shared_value:{self.shared_value.value}, "
            f"shared_array:{self.shared_array[:]}")

    def work_with_shared_memory2(self):
        self.shared_value.value += 5

        for i in range(len(self.shared_array)):
            self.shared_array[i] += 5

        print(
            f"---process_data_shared_memory2---"
            f"shared_value:{self.shared_value.value}, "
            f"shared_array:{self.shared_array[:]}")

    def start_with_shared_memory(self):
        p1 = Process(target=self.work_with_shared_memory1)
        p2 = Process(target=self.work_with_shared_memory2)
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        print(
            f"---start_with_shared_memory---"
            f"shared_value:{self.shared_value.value}, "
            f"shared_array:{self.shared_array[:]}")

    def work_with_semaphore(self, num):

        self.semaphore.acquire()
        print(f"---进程:{num} work_with_semaphore start---")
        time.sleep(1)
        print(f"---进程:{num} work_with_semaphore finish---")
        self.semaphore.release()

    def start_with_semaphore(self):

        procs = [Process(target=self.work_with_semaphore, args=(i,)) for i in range(5)]

        for p in procs:
            p.start()

        for p in procs:
            p.join()

    def start_with_pool(self):

        with Pool(5) as pool:
            res = pool.map(ProcessTest.work_with_pool, [1, 2, 3, 4, 5])
            print(f"---start_with_pool---res:{res}")

        results = []
        with Pool(3) as pool:

            for i in range(1, 10):
                result = pool.apply_async(func=ProcessTest.work_with_pool, args=(i, ))
                results.append(result)

            pool.close()
            pool.join()

            res = [result.get() for result in results]
            print(f"---start_with_pool---res = {res}")


    @staticmethod
    def work_with_pool(num):
        print(f'work_with_pool---进程名{multiprocessing.current_process().name}，进程号{os.getpid()}')
        num += 10
        print(f"work_with_pool = num:{num}")

        time.sleep(2)
        return num
