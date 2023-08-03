#!/usr/bin/python3


class LogInfo(object):

    def __init__(self):
        self.file_name = ""
        self.file_size = 0
        self.log_count = 0
        self.total_time = 0
        self.average_time = 0
        self.log_list = []
        self.log_time_dict = {}
        self.log_time_list = []
        self.log_flag_list = []

    def add_log_info(self, file_name, file_size, time, flag):

        if self.log_count == 0:
            self.file_name = file_name
            self.file_size = file_size
            self.total_time = time
            self.log_count = 1
            self.average_time = round(time, 2)
            self.log_time_list = []
        elif self.file_name == file_name:
            self.log_count += 1
            self.total_time += time
            self.average_time = round(self.total_time / self.log_count, 2)

        self.log_time_list.append(time)
        self.log_flag_list.append(flag)

    def get_log_info(self):
        res = "filename:" + self.file_name + ",file_size:" + str(self.file_size) + "\n"
        # 耗时
        for time in self.log_time_list:
            res += str(time) + "\n"

        res += "average_time:" + str(self.average_time) + "\n"

        # 文件上传状态
        for time in self.log_flag_list:
            res += str(time) + "\n"
        return res


