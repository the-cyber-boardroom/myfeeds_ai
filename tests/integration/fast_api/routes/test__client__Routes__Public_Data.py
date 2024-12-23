from unittest import TestCase

from myfeeds_ai.fast_api.public_data.Public_Data__Fast_API import ROUTES__BASE_PATH__PUBLIC_DATA
from myfeeds_ai.fast_api.public_data.routes.Routes__Public__Hacker_News import ROUTES__TAG__PUBLIC__HACKER_NEWS
from osbot_utils.utils.Dev                        import pprint
from tests.integration.data_feeds__objs_for_tests import data_feeds__fast_api__client


class test__client__Routes__Public_Data(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client      = data_feeds__fast_api__client
        cls.parent_path = f'{ROUTES__BASE_PATH__PUBLIC_DATA}/{ROUTES__TAG__PUBLIC__HACKER_NEWS}'

    def get_response(self, method_name):
        path        = f'{self.parent_path}/{method_name}'
        response = self.client.get(path)
        return response

    def test__hacker_news__ping(self):
        method_name = 'ping'
        response    = self.get_response(method_name)
        assert response.status_code == 200
        assert response.text        == '"pong"'

    def test__hacker_news__data_feed_current(self):
        method_name   = 'latest/feed-data.json'
        response      = self.get_response(method_name)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json.get('created_by') == 'Hacker_News__Files.xml_feed__current'
