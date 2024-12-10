from unittest                                                                               import TestCase
from cbr_custom_data_feeds.data_feeds.Data__Feeds__Shared_Constants                         import S3_FILE_NAME__RAW__CONTENT, S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA, S3_BUCKET_SUFFIX__HACKER_NEWS, S3_BUCKET_PREFIX__DATA_FEEDS
from cbr_custom_data_feeds.data_feeds.models.Model__Data_Feeds__Providers                   import Model__Data_Feeds__Providers
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
        with self.s3_db_oss as _:
            raw_content     = OSS__Http_Content().raw_content()
            result          = _.raw_content__save(raw_content)
            when_str        = _.s3_key_generator.path__for_date_time__now_utc()
            s3_path         = result.get('s3_path')
            s3_key          = _.s3_key__for_provider_path(s3_path)
            assert s3_key == f'{S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA}/{Model__Data_Feeds__Providers.OPEN_SECURITY_SUMMIT.value}/{when_str}/{S3_FILE_NAME__RAW__CONTENT}.json'
            assert _.s3_file_exists(s3_key)
            assert s3_path in _.provider__all_files()

            saved_obj      = _.raw_content__load__now()                             # takes about 27ms in dev
            assert saved_obj.raw_data == raw_content.raw_data
            assert saved_obj.storage_path == s3_path

    def test_s3_path__raw_content__now(self):
        with self.s3_db_oss as _:
            s3_path  = _.s3_path__raw_content__now()
            when_str = _.s3_key_generator.path__for_date_time__now_utc()
            assert s3_path == f'{when_str}/{S3_FILE_NAME__RAW__CONTENT}.json'