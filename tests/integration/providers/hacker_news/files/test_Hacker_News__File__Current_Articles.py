from unittest import TestCase

from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Current_Articles import \
    Hacker_News__File__Current_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles import \
    Schema__Feed__Current_Article__Status
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set
from tests.integration.data_feeds__objs_for_tests import cbr_website__assert_local_stack


class test_Hacker_News__File__Current_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.file_current_articles = Hacker_News__File__Current_Articles()

    def test_group_by_status(self):
        with self.file_current_articles as _:
            assert _.path_latest   () == 'latest/current-articles.json'
            assert _.exists__latest() is True
            for status, articles in  _.group_by_status().items():
                assert status in Schema__Feed__Current_Article__Status.__members__
                for article in articles:
                    assert list_set(article) == ['article_id', 'knowledge_graph', 'llm_prompt', 'location',
                                                 'path__entities_mgraph__json', 'path__entities_mgraph__png',
                                                 'path__feed_article', 'status']
