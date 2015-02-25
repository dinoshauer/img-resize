import io
import os
import time
from urlparse import urlparse

import magic
import redis
import requests
import statsd

import resize

class ImageRetriever:
    def __init__(self, redis_config):
        self.r = redis.Redis(**redis_config)

    def get_file(self, key):
        return self.r.get(key)

class Resizer:
    def __init__(self, redis_config, image_dir, statsd_config=None, key_expire=None):
        self.redis_config = redis_config
        self.r = redis.Redis(**redis_config)
        self.get = requests.get
        self.key_expire = key_expire
        self.image_dir = image_dir
        self.stats_client = statsd.StatsClient(
            statsd_config['host'],
            statsd_config['port'],
        )
        self.statsd_config = statsd_config

    @staticmethod
    def _get(kwargs, key, fallback):
        try:
            return kwargs[key]
        except KeyError:
            return kwargs[fallback]

    def _parse_url(self, url):
        file_name, file_ext = os.path.splitext(
            os.path.basename(
                urlparse(url).path
            )
        )
        return u'{}{}'.format(file_name, file_ext)

    def _check_file_type(self, blob):
        if blob:
            result = magic.from_buffer(blob)
            return 'bitmap' in result or 'image' in result

    def _build_url(self, kwargs):
        url = self._get(kwargs, 'file', 'src')
        for k, v in kwargs.items():
            if k not in ['src', 'file', 'w', 'h', 'width', 'height']:
                url += u'&{k}={v}'.format(k=k, v=v)
        return url

    @staticmethod
    def _check_for_protocol(url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return u'http://{}'.format(url)

    def process_and_return(self, kwargs):
        with self.stats_client.timer(self.statsd_config['process_request_timer']):
            file_name = u'{file_name}_{w}_{h}'.format(
                file_name=self._parse_url(self._get(kwargs, 'file', 'src')),
                w=self._get(kwargs, 'width', 'w'),
                h=self._get(kwargs, 'height', 'h')
            )
            key_name = u'{path}_{w}_{h}'.format(
                path=self._build_url(kwargs),
                w=self._get(kwargs, 'width', 'w'),
                h=self._get(kwargs, 'height', 'h')
            )
            image = ImageRetriever(self.redis_config)
            with self.stats_client.timer(self.statsd_config['get_file_timer']):
                file_exists = image.get_file(key_name)
                if file_exists:
                    self.stats_client.incr(self.statsd_config['cached_counter'])
                    return file_exists
                result = self.process(kwargs, key_name, file_name=file_name)
                if result:
                    return image.get_file(result['file_name'])

    def process(self, kwargs, key_name, file_name=None):
        src = None
        with self.stats_client.timer(self.statsd_config['download_timer']):
            src = self.download_image(self._build_url(kwargs))
        if src:
            w = int(self._get(kwargs, 'width', 'w'))
            h = int(self._get(kwargs, 'height', 'h'))
            with self.stats_client.timer(self.statsd_config['resize_timer']):
                thumb = self.resize_image(src, w, h, file_name)
                if self.to_redis(key_name, thumb):
                    return {'file_name': key_name}

    def to_redis(self, name, thumb):
        with self.stats_client.timer(self.statsd_config['save_file_timer']):
            if self.r.setex(name, self.read_to_bytes(thumb), self.key_expire):
                return self.remove_file(thumb)

    def download_image(self, src):
        request = self.get(self._check_for_protocol(src))
        if request.ok:
            c = request.content
            if self._check_file_type(c):
                return io.BytesIO(c)

    def resize_image(self, src, w, h, file_name):
        out = u'{}/{}_{}'.format(self.image_dir, file_name, time.time())
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
