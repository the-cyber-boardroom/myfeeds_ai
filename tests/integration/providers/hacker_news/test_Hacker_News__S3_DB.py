from unittest                                                                                   import TestCase

from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__S3__Key_Generator  import Hacker_News__S3__Key_Generator
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker__News__S3_DB             import Hacker_News__S3_DB, S3_BUCKET_PREFIX__NEWS_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS
from osbot_utils.helpers.Safe_Id                                                                import Safe_Id
from osbot_utils.utils.Misc                                                                     import random_text
from tests.integration.news_feeds__objs_for_tests                                               import cbr_website__assert_local_stack, CBR_ATHENA__TEST__AWS_ACCOUNT_ID

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

    def test_s3_key(self):
        with self.s3_db_hacker_news as _:
            when_path_elements = _.s3_key_generator.create_path_elements__from_when().pop()
            area               = random_text('area')
            file_id            = 'file-id'
            assert _.s3_key(area=area, file_id='file-id') == f'public-data/{area}/{when_path_elements}/{file_id}.json'