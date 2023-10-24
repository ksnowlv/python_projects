# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from processtest import ProcessTest


def main():
    # Use a breakpoint in the code line below to debug your script.
    pt = ProcessTest()
    pt.start_with_pipe()
    pt.start_with_queue()
    pt.start_with_shared_memory()
    pt.start_with_semaphore()
    pt.start_with_pool()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
