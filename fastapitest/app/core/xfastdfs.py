
from fdfs_client.client import *

g_fast_dfs = None

class XFastDFS(object):

    def __init__(self):
        tracker_conf = get_tracker_conf('app/core/fastdfs_client.conf')
        self.client = Fdfs_client(tracker_conf)
        print(f"Fdfs_client{self.client}")

    def fds_client(self):
        return self.client

    @staticmethod
    def fast_dfs():
        global g_fast_dfs
        if g_fast_dfs is None:
            g_fast_dfs = XFastDFS()

        return g_fast_dfs.fds_client()