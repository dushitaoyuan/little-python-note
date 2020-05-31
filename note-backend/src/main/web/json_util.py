from fastapi.encoders import jsonable_encoder
import json

"""
json处理
"""


class JsonUtil(object):
    @staticmethod
    def toJsonString(data: object = None):
        return jsonable_encoder(data, exclude_none=True)

    @staticmethod
    def parseObject(jsonString: str = None):
        return json.load(jsonString)
