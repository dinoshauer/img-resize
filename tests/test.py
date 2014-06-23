import json
from unittest import TestCase

from httmock import urlmatch, HTTMock
from redis import Redis
import requests

from app import app

import os

# @urlmatch(netloc=r'(.*\.)?test.server\.com$')
# def get_image_mock(url, request):
#     return open('tests/test_resources/heman.png', 'r').read()

# with HTTMock(get_image_mock):
#     r = requests.get('http://test.server.com/heman.png')

class ImageResizeTest(TestCase):
    def setUp(self):
        print "os.environ.get('IMG_RESIZER_TESTING')", os.environ.get('IMG_RESIZER_TESTING')
        print "app.config['TESTING']", app.config['TESTING']
        self.app = app.test_client()

class TestResizeImage(ImageResizeTest):
    def test(self):
        assert 1 == 1
