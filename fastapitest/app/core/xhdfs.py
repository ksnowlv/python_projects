from pywebhdfs.webhdfs import PyWebHdfsClient

g_hdfs = None


class XHDFS(object):

    def __init__(self):
        # self.client = InsecureClient('hdfs://127.0.0.1:9000', user='lvwei')
        # self.client = PyWebHdfsClient(host='127.0.0.1', port=9000, user_name='lvwei')
        self.client = PyWebHdfsClient(host='127.0.0.1', port=9870, user_name='lvwei')
        res = self.client.list_dir("user/lvwei")
        print(f"list_dir:{res}")

    def _hdfs_client(self):
        return self.client

    @staticmethod
    def hdfs():
        global g_hdfs
        if g_hdfs is None:
            g_hdfs = XHDFS()

        return g_hdfs._hdfs_client()
