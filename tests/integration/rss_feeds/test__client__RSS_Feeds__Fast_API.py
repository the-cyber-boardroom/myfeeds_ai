from unittest                                     import TestCase
from tests.integration.data_feeds__objs_for_tests import myfeeds_tests__setup_fast_api__and_localstack


class test__client__RSS_Feeds__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = myfeeds_tests__setup_fast_api__and_localstack().data_feeds__fast_api__client

    # def test__ping(self):
    #     with self.client:
    #         response = self.client.get('/rss-feeds/rss-parser/ping')
    #         assert response.status_code == 200
    #         assert response.json()      == {'it is':  'pong'}