#!/usr/bin/python3

INTERFACE_INFO_LOG_LIST = [[2000, "大于2000ms:"], [1000, "大于1000ms:"], [800, "大于800ms:"],
                           [300, "大于300ms:"], [200, "大于200ms:"], [0, "小于200ms:"]]


class InterfaceInfo(object):
    def __init__(self):
        self.interface_name = ""
        self.log_count = 0
        self.total_time = 0
        self.average_time = 0
        self.log_list = []
        self.log_time_dict = {}
        self.log_time_list = []

    def add_log_info(self, row_data, interface_name, time):

        if self.log_count == 0:
            self.interface_name = interface_name
            self.total_time = time
            self.log_count = 1
            self.average_time = round(time, 2)
            self.log_time_list = []
        elif self.interface_name == interface_name:
            self.log_count += 1
            self.total_time += time
            self.average_time = round(self.total_time / self.log_count, 2)

        for item in INTERFACE_INFO_LOG_LIST:
            if time > item[0]:
                if self.log_time_dict.get(item[0]) is None:
                    self.log_time_dict[item[0]] = 1
                else:
                    self.log_time_dict[item[0]] += 1
                break

        if time > 2000:
            self.log_time_list.append(time)

        if time > 200:
            self.log_list.append(row_data)

    def get_log_info(self):
        return ".接口名称:" + self.interface_name + " 接口请求次数:" + str(self.log_count) + " 接口平均耗时:" + str(
            self.average_time) + "ms\n"

    def get_log_sort_result(self):
        if self.log_time_dict is None:
            return

        log = self.get_log_info()

        for item in INTERFACE_INFO_LOG_LIST:
            if self.log_time_dict.get(item[0]):
                res = item[1] + str(self.log_time_dict.get(item[0])) + "次"
                if item[0] == 2000:
                    res += ",耗时分别是"
                    for j in self.log_time_list:
                        res += str(j) + 'ms,'
                log += res + '\n'

        return log

