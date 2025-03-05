from unittest                                                                                       import TestCase

from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article import Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__All         import Hacker_News__File__Articles__All
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from osbot_utils.utils.Dev import pprint
from tests.integration.data_feeds__objs_for_tests import cbr_website__assert_local_stack


class test_Hacker_News__Article(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cbr_website__assert_local_stack()
    #     cls.file_articles_current = Hacker_News__File__Articles__Current()
    #     cls.file_articles_all     = Hacker_News__File__Articles__All    ()

    def test_file_article(self):
        article_id         = '9153bba8'
        path__folder__data = '1955/11/12/22'
        with Hacker_News__Article(article_id=article_id, path__folder__data=path__folder__data) as _:
            file_article = _.file_article()
            assert file_article.path_now        () == f'{path__folder__data}/articles/{article_id}/feed-article.json'
            assert file_article.folder__path_now() == f'{path__folder__data}/articles/{article_id}'

