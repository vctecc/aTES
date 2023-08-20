import time

import redis
from config import Config


class RedisStream:

    def __init__(self, host: str, port: int, stream: str):
        self._con = redis.Redis(host=host, port=port, charset="utf-8", decode_responses=True)
        self.stream = stream
        self.timestamp = round(time.time() * 1000)

    def save(self, value: dict):
        return self._con.xadd(self.stream, value)

    def xread(self):
        if res := self._con.xread({self.stream: '$'}, block=10, count=None):
            return res[0]
        return []

    def read(self) -> list:
        if res := self._con.xread({self.stream: f"{self.timestamp}-0"}):
            self.timestamp = round(time.time() * 1000)
            return res[0][1]
        return []


user_stream = RedisStream(host=Config.REDIS_HOST, port=Config.REDIS_PORT, stream='user-stream')
