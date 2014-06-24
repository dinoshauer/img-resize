import os
import json
from unittest import TestCase

import requests
from PIL import Image
from httmock import urlmatch, HTTMock
from redis import Redis

from app import app
import config

@urlmatch(netloc=r'(.*\.)?test.server\.com$')
def get_image_mock(url, request):
    return open('tests/test_resources/heman.png', 'r').read()


class ImageResizeTest(TestCase):
    def setUp(self):
        self.r = Redis()
        self.app = app.test_client()
        self.test_image_name = 'test_image.jpg'
        self.base_url = '/v1/resizer/{}'
        self.get_image_url = self.base_url.format(
                    '?width={}&height={}&file={}'.format(
                        0, 100, 'http://test.server.com/heman.png'
                    )
                )
        self.bad_argument_url = self.base_url.format('?file=http://test.server.com/heman.png')

    def tearDown(self):
        self.r.delete('heman.png_0_100')
        try:
            os.remove(self.test_image_name)
        except OSError:
            pass

class TestResizeImage(ImageResizeTest):
    def make_request(self, width, height):
        with HTTMock(get_image_mock):
            response = self.app.get(self.get_image_url)
            image = self.r.get('heman.png_0_100')

            with open(self.test_image_name, 'w') as f:
                f.write(image)

            width, height = Image.open(self.test_image_name).size

            assert response.status_code == 200
            assert 'image/jpeg' in response.content_type

            assert 'heman.png_0_100' in self.r.keys('heman.png_0_100')
            assert image is not None

            return width, height

    def test_file_exists_already(self):
        with HTTMock(get_image_mock):
            response = self.app.get(self.get_image_url)
            with HTTMock(get_image_mock):
                response_2 = self.app.get(self.get_image_url)
                assert response_2.status_code == 200

    def test_height(self):
        width, height = self.make_request(0, 100)
        assert height is not None
        assert width is not None

    def test_width(self):
        width, height = self.make_request(100, 0)
        assert width is not None
        assert height is not None

    def test_bad_argument(self):
        with HTTMock(get_image_mock):
            response = self.app.get(self.bad_argument_url)
            assert response.status_code == 400

class TestUtils(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_ping(self):
        response = self.app.get('/v1/utils/ping')
        assert response.status_code == 200
        assert response.get_data() == 'pong'

class TestConfig(TestCase):
    def setUp(self):
        self.statsd_config = 'statsd_config'
        self._create_statsd_config()

    def tearDown(self):
        try:
            os.remove(self.statsd_config)
        except OSError:
            pass

    def _create_statsd_config(self):
        config = {
            "statsd_host": "localhost",
            "statsd_port": 8125
        }
        with open(self.statsd_config, 'w') as f:
            f.write(json.dumps(config))

    def test_statsd_config(self):
        config._load_statsd_config(app, self.statsd_config)
        statsd = app.config['STATSD']
        assert isinstance(statsd, dict)
        assert statsd['host'] == 'localhost'
        assert statsd['port'] == 8125
