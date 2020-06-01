from web.bytes_string_util import *
from web.password_util import *
from config import GLOBAL_CONFIG

d = b'12314'
hex = to_str(d, StringType.HEX)
print("hex {}, decode hex {}".format(hex, to_bytes(hex, StringType.HEX)))

b64 = to_str(d, StringType.BASE64)
print("base64 {}, decode base64 {}".format(b64, to_bytes(b64, StringType.BASE64)))

b64_safe = to_str(d, StringType.BASE64_URL_SAFE)
print("base64_safe {}, decode base64 {}".format(b64_safe, to_bytes(b64, StringType.BASE64_URL_SAFE)))

encode_password = passwordEncode("123456")
print(encode_password)
print(passwordEq("123456", encode_password))

print(passwordEncode("dushitaoyuan"))

import os
import schedule


def force_pull():
    output = os.popen(
        'cd ' + 'C:\\Users\都市桃源\Desktop\\vertx-web-springmvc' + ' && git fetch --all && git reset --hard origin/master && git pull')
    print(output.read())


force_pull()


def hello():
    print("hello")


schedule.every().seconds.do(hello)
while True:
    schedule.run_pending()
