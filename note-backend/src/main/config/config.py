import configparser
import os
from constant.constants import const

# 计算 项目路径
project_path = os.path.abspath("../");
project_path = str(project_path)[0:project_path.index(const.PROJECT_NAME) + len(const.PROJECT_NAME)]


class SystemConfig(object):

    def __init__(self):
        # 计算 配置路径
        self.config_path = os.path.join(project_path, "src/config/config.ini")
        self.reload()
        self.project_path = project_path

    # 加载配置
    def reload(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='UTF-8')
        self.active_namespace = self.config.get("profiles", "active")
        self.base_namespace = self.config.get("profiles", "base_namespace")

    # 指定配置前缀获取配置项
    def get(self, namespace, key):
        return self.config.get(namespace, key)

    def get(self, key):
        if self.config.has_option(self.active_namespace, key):
            return self.config.get(self.active_namespace, key)
        elif self.config.has_option(self.base_namespace, key):
            return self.config.get(self.base_namespace, key)
        return None

    # 获取当前激活的配置
    def get_active(self, key):
        return self.config.get(self.active_namespace, key)

    # 获取基础配置
    def get_base_config(self, key):
        return self.config.get(self.base_namespace, key)


GLOBAL_CONFIG = SystemConfig()
