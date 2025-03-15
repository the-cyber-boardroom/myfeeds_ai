from unittest                                                           import TestCase
from myfeeds_ai.fast_api.public_data.routes.Routes__Public__Hacker_News import Routes__Public__Hacker_News
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_fast_api__and_localstack

EXPECTED_VALUE__FEED_TITLE     = 'Hacker_News__Files.xml_feed__current'
PATH__PUBLIC_DATA__HACKER_NEWS = '/public-data/hacker-news'

class test__int__Routes__Public__Hacker_News(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client                    = myfeeds_tests__setup_fast_api__and_localstack().data_feeds__fast_api__client
        cls.routes_public_hacker_news = Routes__Public__Hacker_News()


    # def test_latest__feed_data(self):
    #     with self.routes_public_hacker_news as _:
    #         assert _.latest__feed_data().get('duration') > 0

    def test_client__latest__articles_current(self):
        path     = f'{PATH__PUBLIC_DATA__HACKER_NEWS}/latest/articles-current.json'
        response = self.client.get(path)
        assert response.status_code == 200

    def test_client__latest__articles_current__exists(self):
        path     = f'{PATH__PUBLIC_DATA__HACKER_NEWS}/latest/articles-current.json/exists'
        response = self.client.get(path)
        assert response.status_code == 200

    def test_client__latest__articles_current__info(self):
        path       = f'{PATH__PUBLIC_DATA__HACKER_NEWS}/latest/articles-current.json/info'
        response  = self.client.get(path)
        assert response.status_code == 200
        #assert response.json().get('ContentType') == 'application/json; charset=utf-8'

    # def test_client__latest__feed_data(self):
    #     path       = f'{PATH__PUBLIC_DATA__HACKER_NEWS}/latest/feed-data.json'
    #     response  = self.client.get(path)
    #     assert response.json().get('created_by') == EXPECTED_VALUE__FEED_TITLE



