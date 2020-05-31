from loguru import (
    logger,
    _string_parsers as string_parser
)
from config import GLOBAL_CONFIG
from datetime import (
    datetime,
    timedelta
)

"""
calc max_size and time
issue : https://github.com/Delgan/loguru/issues/241

"""


class Rotator:
    def __init__(self, str_size, str_time):
        self._size = string_parser.parse_size(str_size)
        at = string_parser.parse_time(str_time)
        now = datetime.now()
        today_at_time = now.replace(hour=at.hour, minute=at.minute, second=at.second)
        if now >= today_at_time:
            # the current time is already past the target time so it would rotate already
            # add one day to prevent an immediate rotation
            self._next_rotate = today_at_time + timedelta(days=1)
        else:
            self._next_rotate = today_at_time

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size:
            return True
        if message.record["time"].timestamp() > self._next_rotate.timestamp():
            self._next_rotate += timedelta(days=1)
            return True
        return False


def get_logger_config():
    log_filename = GLOBAL_CONFIG.get("log.filename")
    log_max_days = GLOBAL_CONFIG.get("log.log_max_days")
    log_max_size = GLOBAL_CONFIG.get("log.log_max_size")
    log_level = GLOBAL_CONFIG.get("log.log_level")
    if log_filename is None:
        log_filename = GLOBAL_CONFIG.project_path + "/logs/log.log"
    if log_max_days is None:
        log_max_days = "30 days"
    if log_max_size is None:
        log_max_size = "500 MB"
    if log_level is None:
        log_level = "DEBUG"

    size_time_rotator = Rotator(log_max_size, "00:00")
    # 日志配置
    logger.add(log_filename, level=log_level, rotation=size_time_rotator.should_rotate, enqueue=True,
               encoding='utf-8',
               retention=log_max_days)
    return logger


LOG = get_logger_config()
