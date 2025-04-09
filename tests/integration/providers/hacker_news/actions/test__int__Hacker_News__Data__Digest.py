from unittest                                                                          import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data__Digest import Hacker_News__Data__Digest
from tests.integration.data_feeds__objs_for_tests                                      import myfeeds_tests__setup_local_stack


class test__int__Hacker_News__Data__Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.data_digest = Hacker_News__Data__Digest()

    def test_digest_articles(self):
        with self.data_digest as _:
            digest_articles = _.digest_articles()
            assert type(digest_articles) is dict

    def test_digest_articles_ids(self):
        with self.data_digest as _:
            assert type(_.digest_articles__ids()) is set

    def test_digest_articles__view_data(self):
        with self.data_digest as _:
            view_data = _.digest_articles__view_data()
            assert type(view_data) is dict
            #pprint(view_data)
