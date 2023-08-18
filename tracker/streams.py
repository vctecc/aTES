import json
import time
from typing import Any

import redis
from config import Config


class RedisStream:

    def __init__(self, host: str, port: int, stream: str):
        print(host, port)
        self._con = redis.Redis(host=host, port=port, charset="utf-8", decode_responses=True)
        self.stream = stream
        self.timestamp = round(time.time() * 1000)

    def send(self, data: Any):
        return self._con.xadd(self.stream, {'msg': json.dumps(data)})

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
task_stream = RedisStream(host=Config.REDIS_HOST, port=Config.REDIS_PORT, stream='task-life-cycle')
