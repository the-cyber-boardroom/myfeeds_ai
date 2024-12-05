from unittest                                                                       import TestCase
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker__News__S3_DB import Hacker_News__S3_DB, S3_BUCKET_PREFIX__NEWS_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS
from osbot_aws.aws.s3.S3__Key_Generator                                             import S3__Key_Generator
from osbot_utils.context_managers.print_duration import print_duration
from tests.integration.news_feeds__objs_for_tests                                   import cbr_website__assert_local_stack, CBR_ATHENA__TEST__AWS_ACCOUNT_ID

from osbot_utils.utils.Dev import pprint

class test_Hacker_News__S3_DB(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.s3_db_hacker_news = Hacker_News__S3_DB()#setup()            #.setup() will create the DB

    def test__init__(self):
        with self.s3_db_hacker_news as _:
            assert _.bucket_name__prefix == 'news-feeds'
            assert _.bucket_name__suffix == 'hacker-news'
            assert _.save_as_gz             is False
            assert type(_.s3_key_generator) is S3__Key_Generator
            assert _.bucket_name()          == f'{S3_BUCKET_PREFIX__NEWS_FEEDS}-{CBR_ATHENA__TEST__AWS_ACCOUNT_ID}-{S3_BUCKET_SUFFIX__HACKER_NEWS}'
            assert _.bucket_exists()        is True
