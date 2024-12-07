from unittest                                      import TestCase
from cbr_custom_news_feeds.utils.Version           import version__cbr_custom_news_feeds
from tests.integration.news_feeds__objs_for_tests  import news_feeds__fast_api__client


class test__client__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = news_feeds__fast_api__client

    def test_raw__uk__homepage(self):
        response = self.client.get('/info/version')
        assert response.status_code == 200
        assert response.json()      == {'version': version__cbr_custom_news_feeds }

