#!/usr/bin/python3

from interfaceinfo import *
from filemgr import *

HSH_URI_NAME_TAG = "requestPath="
HSH_TIME_COST_TAG = "executeTime="
HSH_FILE_HEADER = "__FILENAME__,__SOURCE__,__TIMESTAMP__"

HZG_URI_NAME_TAG = "Method="
HZG_TIME_COST_TAG = "Time="
HZG_FILE_HEADER = "IP,Method,Request,Time"

# 打包后与应用同级目录logtest.app/Contents/MacOS/
LOG_RESULT_FILE_NAME = "../../../logText.txt"
# LOG_RESULT_FILE_NAME ="logText.txt"

# def my_callbcak(args):
#     print(*args)


class LogMgr(object):

    LOG_STATE_PARSE_LOG_TYPE = 1
    LOG_STATE_LOAD_FILE = 2
    LOG_STATE_PARSE_LOG_DATA = 3
    LOG_STATE_OUTPUT_ALL_RESULT = 4
    LOG_STATE_OUTPUT_SLOW_RESULT = 4

    def __init__(self):
        self.file_name = ''
        self.log_dict = {}
        self.uri_name_tag = ""
        self.time_cost_tag = ""
        self.log_callback = None
        self.log_file_path = FileMgr.resource_path(LOG_RESULT_FILE_NAME)
        FileMgr.del_files(self.log_file_path)

    def load_file(self, file_name, callback):
        self.file_name = file_name
        self.log_callback = callback

        self.log_callback(LogMgr.LOG_STATE_PARSE_LOG_TYPE)
        # 先判断文件内容是属于哪种格式的日志
        with open(self.file_name, 'r', encoding='utf-8', errors='ignore') as file:
            while True:
                line = file.readline()
                print(line)
                if not line:
                    break
                elif line.find(HSH_FILE_HEADER) != -1 or line.find(HZG_FILE_HEADER) != -1:
                    continue
                else:
                    hsh_pos_url = line.find(HSH_URI_NAME_TAG)
                    hsh_pos_time = line.find(HSH_TIME_COST_TAG)
                    hzg_pos_url = line.find(HZG_URI_NAME_TAG)
                    hzg_pos_time = line.find(HZG_TIME_COST_TAG)

                    if hsh_pos_url != -1 and hsh_pos_time != -1:
                        self.uri_name_tag = HSH_URI_NAME_TAG
                        self.time_cost_tag = HSH_TIME_COST_TAG
                        break
                    elif hzg_pos_url != -1 and hzg_pos_time != -1:
                        self.uri_name_tag = HZG_URI_NAME_TAG
                        self.time_cost_tag = HZG_TIME_COST_TAG
                        break
                    else:
                        print("file name not support!!!")

        self.log_callback(LogMgr.LOG_STATE_LOAD_FILE)

        self.log_dict.clear()
        print("load file", self.file_name)

        # 打开文件并逐行处理日志内容，输出日志处理结果
        with open(self.file_name, 'r', encoding='utf-8', errors='ignore') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                else:
                    self.process_line_data(line)
                    self.log_callback(LogMgr.LOG_STATE_PARSE_LOG_DATA)

            self.output_all_result()
            self.log_callback(LogMgr.LOG_STATE_OUTPUT_ALL_RESULT)
            self.output_slow_interface()
            self.log_callback(LogMgr.LOG_STATE_OUTPUT_SLOW_RESULT)

    def process_line_data(self, line):

        pos1 = line.find(self.uri_name_tag)
        if pos1 == -1:
            return
        pos2 = line.find(',', pos1)
        pos3 = line.find(self.time_cost_tag)
        pos4 = line.find('ms', pos3)
        interface_name = line[pos1:pos2]
        time_string = line[pos3 + len(self.time_cost_tag):pos4]

        if len(interface_name) == 0:
            return

        if not time_string.isdigit():
            return

        time = float(time_string)
        item = self.log_dict.get(interface_name)

        if item is None:
            item = InterfaceInfo()
            self.log_dict[interface_name] = item

        item.add_log_info(line, interface_name, time)

    def output_all_result(self):
        log = "----------------接口耗时如下----------\n"
        print(log)
        idx = 0
        for value in self.log_dict.values():
            idx += 1
            res = str(idx) + value.get_log_info()
            log += res

        print("output_all_result", log)
        self.write_log_to_file(log)

    def output_slow_interface(self):
        # 按照值对象的平均时间对字典进行从大到小排序
        sorted_tuples = sorted(self.log_dict.items(), key=lambda x: x[1].average_time, reverse=True)
        res = '----------超过200ms的接口如下----------\n'
        i = 1
        for value in sorted_tuples:
            if value[1].average_time > 200:
                res += str(i) + value[1].get_log_sort_result()
                i += 1
        print("output_slow_interface", res)
        self.write_log_to_file(res)

    # def output_slow_interface(self):
    #     # 按照值对象的平均时间对字典进行排序
    #     sorted_dict = dict(sorted(self.log_dict.items(), key=lambda x: x[1].average_time, reverse=True))
    #     res = '----------超过200ms的接口如下----------\n'
    #     i = 1
    #     for value in sorted_dict.values():
    #         if value.average_time > 200:
    #             res += str(i) + value.get_log_sort_result()
    #             i += 1
    #     print("output_slow_interface", res)
    #     self.write_log_to_file(res)

    def write_log_to_file(self, log_text):

        if log_text:
            with open(self.log_file_path, "ab+") as file:
                file.write(log_text.encode())

