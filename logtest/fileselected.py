#!/usr/bin/python3

from tkinter.filedialog import *


class FileSelected(object):

    @staticmethod
    def askopenfile(mode="r", **options):
        # 返回一个只读文件对象
        file_name = Open(**options).show()
        if file_name:
            return open(file_name, mode)

