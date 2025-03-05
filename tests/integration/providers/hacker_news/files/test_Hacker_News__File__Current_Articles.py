from unittest                                                                                       import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Current_Articles      import Hacker_News__File__Current_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Article__Status  import Schema__Feed__Current_Article__Step
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles         import Schema__Feed__Current_Article
from osbot_utils.utils.Misc                                                                         import list_set
from tests.integration.data_feeds__objs_for_tests                                                   import cbr_website__assert_local_stack

class test_Hacker_News__File__Current_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()


    def setUp(self):
        self.file_current_articles = Hacker_News__File__Current_Articles()
        with self.file_current_articles as _:
            if _.exists__latest() is False:                                                     # check if the file exists
                import pytest
                pytest.skip("test needs a current-articles files in the latest folder")
            _.load()                                                                            # if it exists, load it


    def test_group_by_next_step(self):
        with self.file_current_articles as _:
            assert _.path_latest   () == 'latest/current-articles.json'
            for status, articles in  _.group_by_next_step().items():
                assert status in Schema__Feed__Current_Article__Step.__members__
                assert type(articles) is list
                for article in articles:
                    assert type(article) is Schema__Feed__Current_Article
                    assert list_set(article) == ['article_id', 'next_step',
                                                 'path__entities_mgraph__json','path__entities_mgraph__png', 'path__feed_article',
                                                 'source_location', 'status']
    def test_next_step__1__save_article(self):
        with self.file_current_articles as _:
            next_step_1 = _.next_step__1__save_article()
            if next_step_1:
                assert next_step_1 == _.group_by_next_step().get('STEP__1__SAVE_ARTICLE')

