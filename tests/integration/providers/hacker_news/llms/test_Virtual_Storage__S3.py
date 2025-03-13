from unittest                                                                 import TestCase
from tests.integration.data_feeds__objs_for_tests                             import myfeeds_tests__setup_local_stack
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Virtual_Storage__S3 import Virtual_Storage__S3

from osbot_utils.utils.Dev import pprint


class test_Virtual_Storage__S3(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.virtual_storage = Virtual_Storage__S3()


    def test__init__(self):
       with self.virtual_storage as _:
           assert type(_) is Virtual_Storage__S3




