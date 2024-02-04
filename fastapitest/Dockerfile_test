# 设置基本镜像
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 拷贝项目文件到工作目录
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 加载测试环境的环境变量文件
COPY test.env .env

RUN test
# 暴露端口
#EXPOSE 8081

# 运行 FastAPI 应用程序
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]