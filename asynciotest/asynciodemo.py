
import asyncio


class AsyncioDemo(object):

    def __init__(self):
        self.count = 0

    def __int__(self):
        self.count = 0

    def test(self):
        self.base_use()

    def base_use(self):
        print(f"---base_use---")
        asyncio.run(self.my_coroutine_test())
        print(f"---协程任务组调度---")
        asyncio.run(self.coroutine_tasks())

        print(f"---等待一组协程任务---")
        asyncio.run(self.wait_coroutine_task())

        print(f"---协程之间通过queue进行通信---")
        asyncio.run(self.coroutine_data_communication())

        print(f"使用 asyncio.Event 进行通信")
        asyncio.run(self.event_test())

    async def my_coroutine_test(self):
        print(f"my_coroutine_test start")
        await asyncio.sleep(2)
        print(f"my_coroutine_test finish")

    async def my_task(self, number):
        print(f"task:{number}")

    async def coroutine_tasks(self):

        my_tasks = [asyncio.create_task(self.my_task(i) ) for i in range(10)]
        await asyncio.gather(*my_tasks)
        my_tasks[8].cancel()
        my_tasks[9].cancel()

    async def wait_my_task(self):
        print(f"wait_my_task start")
        await asyncio.sleep(2)
        print(f"wait_my_task end")

    async def wait_coroutine_task(self):
        mytask = [asyncio.create_task(self.wait_my_task()) for _ in range(5)]
        (done, pending) = await asyncio.wait(mytask)
        for task in done:
            print(task.result())

    async def coroutine_data_communication(self):
        queue = asyncio.Queue()
        producer = asyncio.create_task(self.producer(queue))
        consumer = asyncio.create_task(self.consumer(queue))
        await asyncio.gather(producer, consumer)
        print(f"---coroutine_data_communication finish---")

    async def producer(self, queue):
        print(f"---produce coroutine---")
        for i in range(10):
            await queue.put(i)
            print(f"produce:{i}")
            await asyncio.sleep(1)

    async def consumer(self, queue):
        print(f"---consumer coroutine---")
        while True:

            if not queue.empty():
                item = await queue.get()
                print(f"Consumed:{item}")
                self.count = 0
            else:
                self.count += 1
                if self.count >= 3:
                    break

            await asyncio.sleep(1)

    async def event_send(self, event):
        print(f"event event_send---1")
        await asyncio.sleep(2)
        event.set()
        print(f"event event_send---2")

    async def event_rev(self, event):
        print(f"event_rev---1")
        await event.wait()
        print(f"event_rev---2")

    async def event_test(self):
        print(f"event_test---1")
        event = asyncio.Event()
        await asyncio.gather(self.event_send(event), self.event_rev(event))
        print(f"event_test---2")
