#!/usr/bin/python3


from tkinter import *
import queue

from fileselected import *
from concurrent.futures import ThreadPoolExecutor
from logmgr import *


class App(object):
    _shared_theard_pool = ThreadPoolExecutor(max_workers=4)
    _shared_queue = queue.Queue()

    def __init__(self):
        self.log_state = 0
        self.root = None
        self.select_file_button = None
        self.info_label = None
        self.quit_Button = None

    def init_widgets(self, root):
        self.__init__()
        self.root = root
        self.root.title("日志分析")
        self.root.geometry("1000x500")
        self.root.resizable = False

        self.select_file_button = Button(root, text="选择日志文件")
        self.select_file_button["command"] = self.selecte_logfile_event
        self.select_file_button.pack()

        self.info_label = Label(root, text="日志解析完成后，会在该应用同级目录生成结果文件：logText.txt")
        self.info_label.pack()

        self.quit_Button = Button(root, text="退出程序", command=self.exit_event)
        self.quit_Button.pack()

        self.root.after(100, self.update_ui)
        # self.button = Button(self.root, text="click", width=10, command=self.show)
        # self.button.pack(side="top")
        #
        # self.scrollBar = Scrollbar(self.root)
        # self.scrollBar.pack(side="right", fill="y")
        #
        # self.text = Text(self.root, height=10, width=45, yscrollcommand=self.scrollBar.set)
        # self.text.pack(side="top", fill=BOTH, padx=10, pady=10)
        # self.scrollBar.config(command=self.text.yview)
        #
        # # 启动after方法
        # self.root.after(100, self.show_msg)

    def update_ui(self):

        while not App._shared_queue.empty():
            content = App._shared_queue.get()
            print(content)
            self.info_label["text"] = content

        self.root.after(100, self.update_ui)

    # 选择日志文件日志文件名称
    def selecte_logfile_event(self):
        path = FileSelected.askopenfile()
        print(path.name)
        self.select_file_button["text"] = "当前选择文件为:" + path.name
        App._shared_theard_pool.submit(App.__thread_run, path.name, self)

    def exit_event(self):
        App._shared_theard_pool.shutdown(wait=True)
        self.root.destroy()

    def log_state_callback(self, state):

        if self.log_state == state:
            return

        self.log_state = state

        state_list = {
            LogMgr.LOG_STATE_PARSE_LOG_TYPE: "正在解析日志类型，是恒生活日志？还是恒掌柜日志",
            LogMgr.LOG_STATE_LOAD_FILE: "正在加载文件",
            LogMgr.LOG_STATE_PARSE_LOG_DATA: "正在解析文件中每条日志",
            LogMgr.LOG_STATE_OUTPUT_ALL_RESULT: "输出所有接口的耗时情况",
            LogMgr.LOG_STATE_OUTPUT_SLOW_RESULT: "日志解析完成后，会在该应用同级目录生成结果文件：logText.txt"
        }

        App._shared_queue.put(state_list.get(state, None))

    @staticmethod
    def __thread_run(file_name, app):
        App._shared_queue.put("日志数据开始分析")
        mgr = LogMgr()
        mgr.load_file(file_name, app.log_state_callback)


