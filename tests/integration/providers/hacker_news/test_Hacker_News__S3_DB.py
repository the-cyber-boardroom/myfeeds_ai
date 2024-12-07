import pytest
from unittest                                                                                             import TestCase
from osbot_utils.utils.Misc                                                                               import random_text
from tests.integration.news_feeds__objs_for_tests                                                         import cbr_website__assert_local_stack, CBR_ATHENA__TEST__AWS_ACCOUNT_ID
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__S3__Key_Generator            import Hacker_News__S3__Key_Generator, S3_FOLDER__ROOT_FOLDER__HACKER_NEWS
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker__News__S3_DB                       import Hacker_News__S3_DB, S3_BUCKET_PREFIX__NEWS_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed import Model__Hacker_News__Raw_Data__Feed


class test_Hacker_News__S3_DB(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.s3_db_hacker_news = Hacker_News__S3_DB().setup()            #.setup() will create the DB

    def test__init__(self):
        with self.s3_db_hacker_news as _:
            assert _.bucket_name__prefix == 'news-feeds'
            assert _.bucket_name__suffix == 'hacker-news'
            assert _.save_as_gz             is False
            assert type(_.s3_key_generator) is Hacker_News__S3__Key_Generator
            assert _.s3_bucket()            == f'{S3_BUCKET_PREFIX__NEWS_FEEDS}-{CBR_ATHENA__TEST__AWS_ACCOUNT_ID}-{S3_BUCKET_SUFFIX__HACKER_NEWS}'
            assert _.bucket_exists()        is True

    def test_raw_data__feed_xml__save(self):
        with self.s3_db_hacker_news as _:
            with pytest.raises(ValueError, match="Parameter 'raw_data_feed' expected type <class 'cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed.Model__Hacker_News__Raw_Data__Feed'>, but got <class 'str'>"):
                _.raw_data__feed__save('raw_data_feed')
            s3_path                = _.s3_path__raw_data__feed_xml__now()
            feed_xml               = 'the feed_xml'
            raw_data_feed          = Model__Hacker_News__Raw_Data__Feed(feed_xml=feed_xml)
            result                 = _.raw_data__feed__save(raw_data_feed)
            year, month, day, hour = _.s3_key_generator.path__for_date_time__now_utc().split('/')
            #s3_path                = _.s3_key_generator.s3_path(year, month, day, hour, 'feed_xml')

            assert result                                            == dict(s3_path= s3_path, file_data= raw_data_feed.json(),save_status = True  )
            assert s3_path                                           in _.raw_data__all_files()
            assert _.raw_data__feed__load__current()         .json() == raw_data_feed.json()
            assert _.raw_data__feed__load__from_path(s3_path).json() == raw_data_feed.json()


    #                               2024/12/06/22/feed_xml.json
    'hacker-news__rss-feed/raw-data/2024/12/06/22/feed_xml.json'

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
            assert s3_key == f'{S3_FOLDER__ROOT_FOLDER__HACKER_NEWS}/raw-data/{when_path}/feed_xml.json'

