from unittest                                                                          import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data__Digest import Hacker_News__Data__Digest


class test__int__Hacker_News__Data__Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_digest = Hacker_News__Data__Digest()

    def test_digest_articles(self):
        with self.data_digest as _:
            digest_articles = _.digest_articles()
            assert type(digest_articles) is dict
            from osbot_utils.utils.Dev import pprint
            # for _,article in digest_articles.items():
            #     pprint(article.json())


    def test_digest_articles_ids(self):
        with self.data_digest as _:
            assert type(_.digest_articles_ids()) is set
