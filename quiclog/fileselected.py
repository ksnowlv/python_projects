#!/usr/bin/python3

from tkinter.filedialog import *


class FileSelected(object):

    @staticmethod
    def askopenfile(mode="r", **options):

        # 返回一个只读文件对象
        filename = Open(**options).show()

        if filename:
            return open(filename, mode)

