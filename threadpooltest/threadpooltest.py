import threading
from concurrent.futures import ThreadPoolExecutor

class ThreadPoolTest(object):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)
        pass

    def __del__(self):
        # self.thread_pool_executor.shutdown()
        pass

    def _task(self, task_name):
        print(f"thread id = {threading.get_ident()}, task_name:{task_name}")
        return task_name

    def start(self):

        for i in range(10):
            future =  self.executor.submit(self._task, "task_name" + str(i))
            print(future.result())
