from unittest                                                                                       import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles                 import Schema__Feed__Article
from osbot_utils.utils.Misc                                                                         import list_set
from tests.integration.data_feeds__objs_for_tests                                                   import myfeeds_tests__setup_local_stack

class test_Hacker_News__File__Current_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()


    def setUp(self):
        self.file_current_articles = Hacker_News__File__Articles__Current()
        with self.file_current_articles as _:
            if _.exists__latest() is False:                                                     # check if the file exists
                import pytest
                pytest.skip("test needs a current-articles files in the latest folder")
            _.load()                                                                            # if it exists, load it


    def test_group_by_next_step(self):
        with self.file_current_articles as _:
            assert _.path_latest   () == 'latest/articles-current.json'
            for status, articles in  _.group_by_next_step().items():
                assert status in Schema__Feed__Article__Step.__members__
                assert type(articles) is list
                for article in articles:
                    assert type(article) is Schema__Feed__Article
                    assert list_set(article) == ['article_id'                            ,
                                                 'next_step'                             ,
                                                 'path__file__entities_mgraph__json'     ,
                                                 'path__file__entities_mgraph__png'      ,
                                                 'path__file__feed_article'              ,
                                                 'path__file__markdown'                  ,
                                                 'path__file__text_entities__description',
                                                 'path__file__text_entities__title'      ,
                                                 'path__file__text_entities__title__png' ,
                                                 'path__folder__data'                    ,
                                                 'path__folder__source'                  ,
                                                 'status'                                ]
    def test_next_step__1__save_article(self):
        with self.file_current_articles as _:
            next_step_1 = _.next_step__1__save_article()
            if next_step_1:
                assert next_step_1 == _.group_by_next_step().get('STEP__1__SAVE__ARTICLE')

