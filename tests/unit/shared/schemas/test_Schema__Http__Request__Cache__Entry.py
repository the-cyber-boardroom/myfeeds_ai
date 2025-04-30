from unittest                                                           import TestCase
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Entry import Schema__Http__Request__Cache__Entry
from osbot_utils.utils.Objects                                          import __

class test_Schema__Http__Request__Cache__Entry(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.http_request_data = Schema__Http__Request__Cache__Entry()

    def test__init__(self):
        with self.http_request_data as _:
            assert type(_) == Schema__Http__Request__Cache__Entry
            assert _.obj() == __(cache_id  = _.cache_id ,
                                 request   = None       ,
                                 response  = None       ,
                                 timestamp = _.timestamp)