import os

import redis
import requests

import resize


class Resizer:
    def __init__(self, redis_config):
        self.r = redis.Redis(**redis_config)

    def

    def read_to_bytes(self, src):
        with open(src, 'rb') as f:
            return f.read()

    def remove_file(self, src):
        try:
            os.remove(src)
            return True
        except IOError:
            return False
