#!/usr/bin/python3
from tkinter import *
import queue

from fileselected import *
from concurrent.futures import ThreadPoolExecutor
from logmgr import *


class App(object):
    _shared_thread_pool = ThreadPoolExecutor(max_workers=2)
    _shared_queue = queue.Queue()

    def __init__(self, root):
        self.state = 0
        self.root = root
        self.root.title("日志分析")
        self.root.geometry("1000x500")
        self.root.resizable = False

        self.select_file_button = Button(self.root, text="选择日志文件")
        self.select_file_button["command"] = self.selected_logfile_event
        self.select_file_button.pack()

        self.info_label = Label(self.root, text="日志解析完成后，会在该应用同级目录生成结果文件：logText.txt")
        self.info_label.pack()

        self.quit_button = Button(self.root, text="退出程序", command=self.exit_event)
        self.quit_button.pack()

        self.root.after(100, self.update_ui)

    def update_ui(self):
        while not App._shared_queue.empty():
            content = App._shared_queue.get()
            # print(content)
            self.info_label["text"] = content

        self.root.after(10, self.update_ui)

    # 选择日志文件日志文件名称
    def selected_logfile_event(self):
        path = FileSelected.askopenfile()
        print(path.name)
        self.select_file_button["text"] = "当前选择文件为:" + path.name
        App._shared_thread_pool.submit(App.__thread_run, path.name, self)

    def exit_event(self):
        App._shared_thread_pool.shutdown(wait=True)
        self.root.destroy()

    def log_state_callback(self, state):

        if self.state == state:
            return

        self.state = state

        App._shared_queue.put(LogMgr.STATE_LIST.get(state))

    @staticmethod
    def __thread_run(file_name, app):
        App._shared_queue.put("日志数据开始分析")
        mgr = LogMgr()
        mgr.load_file(file_name, app.log_state_callback)


