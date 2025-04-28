from datetime                                                                               import datetime
from unittest                                                                               import TestCase
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File__Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article  import Hacker_News__Storage__Article, S3_FOLDER_NAME__ARTICLES
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article       import Hacker_News__File__Article
from osbot_utils.helpers.Obj_Id                                                             import Obj_Id
from osbot_utils.helpers.Safe_Id                                                            import Safe_Id
from tests.integration.data_feeds__objs_for_tests                                           import myfeeds_tests__setup_local_stack

from osbot_utils.utils.Dev import pprint


class test_Hacker_News__File__Article(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.article_id      = Obj_Id()
        self.file_id         = Safe_Id("an-file-in-article")
        self.file_article    = Hacker_News__File__Article(article_id=self.article_id, file_id=self.file_id)
        self.folder_path_now = self.file_article.folder__path_now()

    def test__init__(self):

        with self.file_article as _:
            assert self.article_id      == _.hacker_news_storage.article_id
            assert self.file_id         == _.file_id
            assert self.folder_path_now == f'{_.hacker_news_storage.s3_db.s3_path__now()}/{S3_FOLDER_NAME__ARTICLES}/{self.article_id}'
            assert _.path_now()         == f'{_.folder__path_now()}/{self.file_id}.json' # BUG, should have /article/{self.article_id}

        with self.file_article.hacker_news_storage as _:
            assert type(_) is Hacker_News__Storage__Article
            assert _.areas() == ['articles', self.article_id]
            date_time = datetime(year=1955, month=11, day=12, hour=22)
            expected_path = f"1955/11/12/22/articles/{self.article_id}/{self.file_id}.mgraph.dot"
            assert expected_path == _.path__date_time(date_time, self.file_id, S3_Key__File__Extension.MGRAPH__DOT)


