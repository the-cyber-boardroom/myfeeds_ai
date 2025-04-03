from unittest                                                                                   import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                  import Hacker_News__Data
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__New     import Hacker_News__File__Articles__New
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Config__New_Articles import Schema__Feed__Config__New_Articles
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack


class test__int__Hacker_News__Data(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.hacker_news_data = Hacker_News__Data()


    def test_new_articles(self):
        with self.hacker_news_data as _:
            new_articles = _.new_articles()
            assert type(new_articles) is Schema__Feed__Config__New_Articles
            assert new_articles.json() == Hacker_News__File__Articles__New().data().json()

    def test_digest_articles(self):
        with self.hacker_news_data as _:
            digest_articles = _.digest_articles()
            assert type(digest_articles) is dict


    def test_digest_articles_ids(self):
        with self.hacker_news_data as _:
            assert type(_.digest_articles_ids()) is set