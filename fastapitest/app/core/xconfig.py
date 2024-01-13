from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str
    MYSQL_DATABASE_URL: str
    GRIDFS_URL: str
    debug: bool

class XConfig(object):
    PROJECT_NAME: str = "fastapitest"
    VERSION = "1.0.0"
    API_PREFIX = "/api"

    def __init__(self):

        # 选择使用测试环境还是生产环境的配置文件
        print(os.environ.get('PYTHONUNBUFFERED'))
        print(os.environ.get('ENVTYPE'))

        env_type = os.environ.get("ENVTYPE")

        if env_type == "prod":
            config_file = "prod.env"
        elif env_type == "test":
            config_file = "test.env"

        # 通过python-dotenv加载指定的配置文件
        load_dotenv(dotenv_path=config_file)

        # 从环境变量中读取配置
        self.settings = Settings()
        print(f"{self.settings}")

    def all_settings(self):
        return self.settings

    @staticmethod
    def shared_config():
        return shared_config

    @staticmethod
    def redis_url():
        return shared_config.all_settings().REDIS_URL


    @staticmethod
    def mysql_database_url():
        return shared_config.all_settings().MYSQL_DATABASE_URL

    @staticmethod
    def gridfs_url():
        return shared_config.all_settings().GRIDFS_URL

    @staticmethod
    def debug():
        return shared_config.all_settings().debug

shared_config = XConfig()
