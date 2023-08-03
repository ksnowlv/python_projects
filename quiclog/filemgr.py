#!/usr/bin/python3

import os
import sys


class FileMgr(object):

    @staticmethod
    def log_file_path(file_name):

        return os.path.join(FileMgr.app_path(), "logfile", file_name)

    @staticmethod
    def app_path():

        if hasattr(sys, 'frozen'):
            # 使用pyinstaller打包后的exe目录
            return os.path.dirname(sys.executable)
        # 正常运行路径
        return os.path.dirname(__file__)

    # 生成资源文件目录访问路径
    # 说明： pyinstaller工具打包的可执行文件，运行时sys。frozen会被设置成True
    #      因此可以通过sys.frozen的值区分是开发环境还是打包后的生成环境
    #
    #  打包后的生产环境，资源文件都放在sys._MEIPASS目录下
    #  修改main.spec中的datas，
    #  如datas=[('res', 'res')]，意思是当前目录下的res目录加入目标exe中，在运行时放在零时文件的根目录下，名称为res

    @staticmethod
    def resource_path(relative_path):
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller 打包后的临时目录
                base_path = sys._MEIPASS
            else:
                # 普通安装的路径
                base_path = os.path.abspath(".")
        else:
            # 普通安装的路径
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @staticmethod
    def del_files(dir_path):
        if os.path.isfile(dir_path):
            try:
                # 这个可以删除单个文件，不能删除文件夹
                os.remove(dir_path)
            except BaseException as e:
                print(e)
        elif os.path.isdir(dir_path):
            file_list = os.listdir(dir_path)
            for file_name in file_list:
                tf = os.path.join(dir_path, file_name)
                FileMgr.del_files(tf)
