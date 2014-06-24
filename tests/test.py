import json
from unittest import TestCase

import requests
from PIL import Image
from httmock import urlmatch, HTTMock
from redis import Redis

from app import app

import os

@urlmatch(netloc=r'(.*\.)?test.server\.com$')
def get_image_mock(url, request):
    return open('tests/test_resources/heman.png', 'r').read()


class SuccessImageResizeTest(TestCase):
    def setUp(self):
        self.r = Redis()
        self.app = app.test_client()
        self.base_url = '/v1/resizer/{}'
        self.test_image_name = 'test_image.jpg'

    def tearDown(self):
        self.r.flushall()
        try:
            os.remove(self.test_image_name)
        except OSError:
            pass

class TestResizeImage(SuccessImageResizeTest):
    def make_request(self, width, height):
        with HTTMock(get_image_mock):
            response = self.app.get(
                self.base_url.format(
                    '?width={}&height={}&file={}'.format(
                        0, 100, 'http://test.server.com/heman.png'
                    )
                )
            )
            image = self.r.get('heman.png_0_100')

            with open(self.test_image_name, 'w') as f:
                f.write(image)

            width, height = Image.open(self.test_image_name).size

            assert response.status_code == 200
            assert 'image/jpeg' in response.content_type

            assert 'heman.png_0_100' in self.r.keys('heman.png_0_100')
            assert image is not None

            return width, height

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
            response = self.app.get(
                self.base_url.format('?file=http://test.server.com/heman.png')
            )
            assert response.status_code == 400
