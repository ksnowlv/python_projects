#!/usr/bin/python3

from logInfo import *
from filemgr import *

# 日志格式：2023-07-21 18:44:15,1001-4.mp4,7.30 MB,11119,1

# 打包后与应用同级目录log_test.app/Contents/MacOS/
# LOG_RESULT_FILE_NAME ="../../../logText.txt"
LOG_RESULT_FILE_NAME = "../logText.txt"


class LogMgr(object):
    NAME_TAG = ".mp4"

    LOG_STATE_LOAD_FILE = 1
    LOG_STATE_PARSE_LOG_DATA = 2
    LOG_STATE_OUTPUT_ALL_RESULT = 3

    STATE_LIST = {
        LOG_STATE_LOAD_FILE: "正在加载文件",
        LOG_STATE_PARSE_LOG_DATA: "正在解析文件中每条日志",
        LOG_STATE_OUTPUT_ALL_RESULT: "日志解析完成后，会在该应用同级目录生成结果文件：logText.txt",
    }

    def __init__(self):
        self.file_name = ''
        self.log_dict = {}
        self.time_cost_tag = ""
        self.log_callback = None
        self.log_file_path = FileMgr.resource_path(LOG_RESULT_FILE_NAME)
        FileMgr.del_files(self.log_file_path)

    def load_file(self, file_name, callback):
        self.file_name = file_name
        self.log_callback = callback
        self.log_callback(LogMgr.LOG_STATE_LOAD_FILE)

        self.log_dict.clear()

        # 打开文件并逐行处理日志内容，输出日志处理结果
        with open(self.file_name, 'r', encoding='utf-8', errors='ignore') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                else:
                    self.log_callback(LogMgr.LOG_STATE_PARSE_LOG_DATA)
                    self.process_line_data(line)

            self.output_all_result()
            self.log_callback(LogMgr.LOG_STATE_OUTPUT_ALL_RESULT)

    def process_line_data(self, line):

        pos1 = line.find(LogMgr.NAME_TAG)
        if pos1 == -1:
            return

        res = line.split(',')
        # 2023-07-21 18:44:15,1001-4.mp4,7.30 MB,11119,1
        if len(res) != 5:
            return

        file_name = res[1]
        file_size = res[2]
        time_string = res[3]
        flag = res[4].replace("\n", "")

        if not time_string.isdigit():
            return

        time = float(time_string)
        item = self.log_dict.get(file_name)

        if item is None:
            item = LogInfo()
            self.log_dict[file_name] = item

        item.add_log_info(file_name, file_size, time, flag)

    def output_all_result(self):
        log = "----------------日志分析结果如下----------\n"
        print(log)
        idx = 0
        for value in self.log_dict.values():
            idx += 1
            res = str(idx) + "." + value.get_log_info()
            print(res)
            log += res

        self.write_log_to_file(log)

    def write_log_to_file(self, log_text):

        if log_text:
            with open(self.log_file_path, "ab+") as file:
                file.write(log_text.encode())



