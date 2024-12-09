import pytest
from unittest                                                                                               import TestCase
from cbr_custom_data_feeds.config.Custom_News__Shared_Constants                                             import S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA, S3_FILE_NAME__RAW__FEED_XML
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__Parser                         import Hacker_News__Parser
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed       import Model__Hacker_News__Data__Feed
from cbr_custom_data_feeds.providers.models.Model__Data_Feeds__Providers                                    import Model__Data_Feeds__Providers
from osbot_utils.utils.Misc                                                                                 import random_text
from osbot_utils.utils.Objects                                                                              import obj
from tests.integration.data_feeds__objs_for_tests                                                           import cbr_website__assert_local_stack, DATA_FEEDS__TEST__AWS_ACCOUNT_ID
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__S3__Key_Generator              import Hacker_News__S3__Key_Generator
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__S3_DB                          import Hacker_News__S3_DB, S3_BUCKET_PREFIX__DATA_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed   import Model__Hacker_News__Raw_Data__Feed
from tests.integration.data_feeds__test_data                                                                import TEST_DATA__HACKER_NEWS__FEED_XML


class test_Hacker_News__S3_DB(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.s3_db_hacker_news = Hacker_News__S3_DB().setup()            #.setup() will create the DB

    def test__init__(self):
        with self.s3_db_hacker_news as _:
            assert _.bucket_name__prefix == 'data-feeds'
            assert _.bucket_name__suffix == 'data'
            assert _.save_as_gz             is False
            assert type(_.s3_key_generator) is Hacker_News__S3__Key_Generator
            assert _.s3_bucket()            == f'{S3_BUCKET_PREFIX__DATA_FEEDS}-{DATA_FEEDS__TEST__AWS_ACCOUNT_ID}-{S3_BUCKET_SUFFIX__HACKER_NEWS}'
            assert _.bucket_exists()        is True

    #@print_boto3_calls()
    def test_feed_data__save(self):
        with self.s3_db_hacker_news as _:
            feed_xml               = TEST_DATA__HACKER_NEWS__FEED_XML
            raw_data_feed          = Model__Hacker_News__Raw_Data__Feed(feed_xml=feed_xml)                                       # todo: this needs to be refactore to a helper class that creates these objects
            parser                 = Hacker_News__Parser().setup(raw_data_feed.feed_xml)
            data_feed              = Model__Hacker_News__Data__Feed    (feed_data=parser.parse_feed())                           # todo: fix this creation since there are values from Model__Hacker_News__Raw_Data__Feed that are missing here
            result                 = obj(_.feed_data__save(data_feed))
            s3_path                = _.s3_path__raw_data__feed_data__now   ()
            s3_path_latest         = _.s3_path__raw_data__feed_data__latest()

            year, month, day, hour = _.s3_key_generator.path__for_date_time__now_utc().split('/')
            all_files              = _.raw_data__all_files()
            file_data__current     = _.feed_data__load__current().obj()
            file_data__from_data   = _.feed_data__load__from_date(year, month, day, hour).obj()
            file_data__latest      = _.feed_data__load__from_path(s3_path_latest).obj()

            assert s3_path                                in all_files
            assert s3_path_latest                         in all_files
            assert result.s3_path                         == s3_path
            assert result.file_data.feed_data.description == 'Security News'
            assert file_data__current                     == result.file_data
            assert file_data__from_data                   == result.file_data
            assert file_data__latest                      == result.file_data

    def test_raw_data__feed_xml__save(self):
        with self.s3_db_hacker_news as _:
            with pytest.raises(ValueError, match="Parameter 'raw_data_feed' expected type <class 'cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed.Model__Hacker_News__Raw_Data__Feed'>, but got <class 'str'>"):
                _.raw_data__feed__save('raw_data_feed')
            feed_xml               = TEST_DATA__HACKER_NEWS__FEED_XML
            raw_data_feed          = Model__Hacker_News__Raw_Data__Feed(feed_xml=feed_xml)                              # todo: this needs to be refactored to a helper class that creates these objects
            raw_data_feed_json     = raw_data_feed.json()
            result                 = _.raw_data__feed__save(raw_data_feed)
            year, month, day, hour = _.s3_key_generator.path__for_date_time__now_utc().split('/')
            s3_path                = _.s3_key_generator.s3_path(year, month, day, hour, S3_FILE_NAME__RAW__FEED_XML)
            s3_path_latest         = _.s3_path__raw_data__feed_xml__latest()
            all_files              = _.raw_data__all_files()
            file_data__current     = _.raw_data__feed__load__current  (              ).json()
            file_data__from_path   = _.raw_data__feed__load__from_path(s3_path       ).json()
            file_data__latest      = _.raw_data__feed__load__from_path(s3_path_latest).json()
            expected_result        = dict( file_data= raw_data_feed.json(),
                                           s3_path= s3_path               )

            assert result               == expected_result
            assert s3_path              in all_files
            assert s3_path_latest       in all_files
            assert file_data__current   == raw_data_feed_json
            assert file_data__from_path == raw_data_feed_json
            assert file_data__latest    == raw_data_feed_json


    def test_s3_key(self):
        with self.s3_db_hacker_news as _:
            area               = random_text('area')
            when_path_elements = '/'.join(_.s3_key_generator.create_path_elements__from_when(area=area))
            file_id            = 'file-id'
            assert _.s3_key_generator.s3_key(area=area, file_id='file-id') == f'{when_path_elements}/{file_id}.json'

    def test_s3_key__for_raw_data__feed_xml(self):
        with self.s3_db_hacker_news as _:
            s3_key    = _.s3_key__raw_data__feed_xml()
            when_path = _.s3_key_generator.path__for_date_time__now_utc().replace('-', '/')
            assert len(when_path.split('/')) == 4
            assert s3_key == f'{S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA}/{Model__Data_Feeds__Providers.HACKER_NEWS.value}/{when_path}/{S3_FILE_NAME__RAW__FEED_XML}.json'

