from unittest                                                                 import TestCase

from myfeeds_ai.data_feeds.Data_Feeds__S3_DB import Data_Feeds__S3_DB
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
            assert _.root_folder == "llm-cache/data/"

        with self.virtual_storage.s3_db as _:
            assert type(_)       is Data_Feeds__S3_DB
            assert _.s3_bucket() == "data-feeds-000011110000-data"

    def test_get_s3_key(self):
        with self.virtual_storage as _:
            assert _.get_s3_key('abc') == 'llm-cache/data/abc'

    def test_json__save(self):
        with self.virtual_storage as _:
            path = 'pytest/an-file.json'
            data = {'a': 42}
            result = _.json__save(path=path, data=data)
            assert result is True
            assert _.file__exists(path   ) is True
            assert _.json__load(path=path) == data
            assert _.file__delete(path   ) is True
            assert _.file__exists(path   ) is False

    # todo: add test for pprint(_.files__all()) and pprint(_.stats()) (create a temp bucket or root folder for this, so that we don't catch the cache files that will be created in the LocalStack test server)





