import os
import uuid
import io

import redis
import requests

import resize

class ImageRetriever:
    def __init__(self, redis_config):
        self.r = redis.Redis(**redis_config)

    def get_file(self, key):
        return self.r.get(key)

class Resizer:
    def __init__(self, redis_config, image_dir, key_expire=None):
        self.r = redis.Redis(**redis_config)
        self.get = requests.get
        self.key_expire = key_expire
        self.image_dir = image_dir

    def _check_redis_for_file(self, file_name):
        return self.r.get(filename)

    def pass_through(self, kwargs):
        file_name = self._parse_url(kwargs['url'])
        file_exists = self._check_redis_for_file(file_name)
        if file_exists:
            return file_exists


    def process(self, kwargs, file_name=None):
        src = self.download_image(kwargs['src'])
        w = int(kwargs['w'])
        h = int(kwargs['h'])
        thumb = self.resize_image(src, w, h, file_name)
        base_name = os.path.basename(thumb)
        if self.to_redis(base_name, thumb):
            return {'filename': base_name}

    def to_redis(self, name, thumb):
        if self.r.setex(name, self.read_to_bytes(thumb), self.key_expire):
            return self.remove_file(thumb)
        return False

    def download_image(self, src):
        request = self.get(src)
        if request.ok:
            return io.BytesIO(request.content)

    def resize_image(self, src, w, h, file_name=None):
        if file_name:
            out = '{}/{}.jpg'.format(self.image_dir, file_name)
        else:
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
