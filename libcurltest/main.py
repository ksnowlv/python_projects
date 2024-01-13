# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pycurl

def test_curl():
    # Use a breakpoint in the code line below to debug your script.
    # 创建 Curl 对象
    curl = pycurl.Curl()

    # 设置 URL
    curl.setopt(pycurl.URL, 'http://127.0.0.1:8081/user/home')

    # 设置请求头
    curl.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])

    # 执行请求
    curl.perform()

    # 获取响应信息
    response_code = curl.getinfo(pycurl.RESPONSE_CODE)
    response_headers = curl.getinfo(pycurl.HEADER_OUT)
    response_body = curl.getvalue()

    print(f"response_code = {response_code}, response_headers= {response_headers}, response_body= {response_body} ")

    # 清理资源
    curl.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_curl()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
