import os
import uuid
import io
from urlparse import urlparse

import redis
import requests
import magic

import resize

class ImageRetriever:
    def __init__(self, redis_config):
        self.r = redis.Redis(**redis_config)

    def get_file(self, key):
        return self.r.get(key)

class Resizer:
    def __init__(self, redis_config, image_dir, key_expire=None):
        self.redis_config = redis_config
        self.r = redis.Redis(**redis_config)
        self.get = requests.get
        self.key_expire = key_expire
        self.image_dir = image_dir

    def _parse_url(self, url):
        file_name, file_ext = os.path.splitext(
            os.path.basename(
                urlparse(url).path
            )
        )
        return '{}{}'.format(file_name, file_ext)

    def _check_file_type(self, blob):
        if blob:
            result = magic.from_buffer(blob)
            return 'bitmap' in result or 'image' in result
        return False

    def process_and_return(self, kwargs):
        file_name = self._parse_url(kwargs['src'])
        image = ImageRetriever(self.redis_config)
        file_exists = image.get_file(file_name)
        if file_exists:
            return file_exists
        result = self.process(kwargs, file_name=file_name)
        if result:
            return image.get_file(result['file_name'])
        return False

    def process(self, kwargs, file_name=None):
        src = self.download_image(kwargs['src'])
        if src:
            w = int(kwargs['w'])
            h = int(kwargs['h'])
            thumb = self.resize_image(src, w, h, file_name)
            base_name = os.path.basename(thumb)
            if self.to_redis(base_name, thumb):
                return {'file_name': base_name}
        return False

    def to_redis(self, name, thumb):
        if self.r.setex(name, self.read_to_bytes(thumb), self.key_expire):
            return self.remove_file(thumb)
        return False

    def download_image(self, src):
        request = self.get(src)
        if request.ok:
            c = request.content
            if self._check_file_type(c):
                return io.BytesIO(c)
        return False

    def resize_image(self, src, w, h, file_name=None):
        if file_name:
            out = '{}/{}'.format(self.image_dir, file_name)
        else:
            out = '{}/{}.jpg'.format(self.image_dir, str(uuid.uuid4()))
        if h is 0 or w is 0:
            result = resize.resize_with_specific_ratio(src, out, width=w, height=h)
        else:
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
