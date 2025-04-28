from unittest import TestCase

from myfeeds_ai.shared.schemas.Schema__My_Feeds__HTTP__Request__Data import Schema__My_Feeds__HTTP__Request__Data
from osbot_utils.utils.Objects import __


class test_Schema__My_Feeds__HTTP__Request__Data(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.http_request_data = Schema__My_Feeds__HTTP__Request__Data()

    def test__init__(self):
        with self.http_request_data as _:
            assert type(_) == Schema__My_Feeds__HTTP__Request__Data
            assert _.obj() == __(content_type   = None       ,
                                 duration       = None       ,
                                 etag           = None       ,
                                 html__dict     = None       ,
                                 json__data     = None       ,
                                 last_modified  = None       ,
                                 method         = None       ,
                                 status_code    = None       ,
                                 text           = None       ,
                                 text__hash     = None       ,
                                 timestamp      = _.timestamp,
                                 url            = None       ,
                                 url__hash      = None       )