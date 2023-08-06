
import queue
import qthread
from qthread import *

# 来源于qthread文件中的s_running
# 多线程调用下需要考虑线程安全，此处仅仅演示跨文件调用全局变量使用
global s_running


def main():

    # 演示生产者消费者示例
    lock = threading.Lock()
    q = queue.Queue(10)
    producer = QThreadProducer('ksnowlv', q, lock)
    consumer1 = QThreadConsumer('kair', q, lock)
    consumer2 = QThreadConsumer('ksnow', q, lock)

    producer.start()
    consumer1.start()
    consumer2.start()

    time.sleep(10)

    # 多线程调用下需要考虑线程安全，此处仅仅演示跨文件调用全局变量使用
    # 不带qthread.直接对s_running赋值在其它文件不生效，必须指定qthread.
    qthread.s_running = False

    producer.stop()
    consumer1.stop()
    consumer2.stop()
    print("queue_test exit")

    producer.join()
    consumer1.join()
    consumer2.join()
    print("thread exit")


if __name__ == '__main__':
    main()
