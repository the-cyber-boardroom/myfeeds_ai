from unittest import TestCase

from cbr_custom_data_feeds.config.Custom_News__Shared_Constants                             import S3_BUCKET_PREFIX__DATA_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Http_Content  import OSS__Http_Content
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__S3_DB         import OSS__S3_DB
from tests.integration.data_feeds__objs_for_tests                                           import cbr_website__assert_local_stack, DATA_FEEDS__TEST__AWS_ACCOUNT_ID


class test_OSS__S3_DB(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.s3_db_oss = OSS__S3_DB().setup()            #.setup() will create the DB

    def test__init__(self):
        with self.s3_db_oss as _:
            assert _.bucket_name__prefix == 'data-feeds'
            assert _.bucket_name__suffix == 'data'
            assert _.save_as_gz             is False
            assert _.s3_bucket()            == f'{S3_BUCKET_PREFIX__DATA_FEEDS}-{DATA_FEEDS__TEST__AWS_ACCOUNT_ID}-{S3_BUCKET_SUFFIX__HACKER_NEWS}'
            assert _.bucket_exists()        is True

    def test_raw_data_save(self):
        raw_content     = OSS__Http_Content().raw_content()
        result          = self.s3_db_oss.raw_content__save(raw_content)
        assert result > 700
