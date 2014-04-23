import os
import uuid

import redis
import requests

import resize


class Resizer:
    def __init__(self, redis_config, image_dir):
        self.r = redis.Redis(**redis_config)
        self.get = requests.get
        self.image_dir = image_dir

    def process(self, kwargs):
        print kwargs
        return {'status': 'ok'}, 200

    def get_image(self, src):
        request = self.get(src)
        if request.ok:
            for c in request.iter_content:
                print c
                print '*****~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*****'

    def resize_image(self, src, w, h):
        out = '{}/{}.jpg'.format(self.image_dir, str(uuid.uuid4()))
        result = resize.resize(src, out, w, h)
        if result:
            return out

    def read_to_bytes(self, src):
        with open(src, 'rb') as f:
            return f.read()

    def remove_file(self, src):
        try:
            os.remove(src)
            return True
        except IOError:
            return False
