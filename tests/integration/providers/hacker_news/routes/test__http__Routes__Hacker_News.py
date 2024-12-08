from unittest                                                                               import TestCase
from osbot_fast_api.utils.Fast_API_Server                                                   import Fast_API_Server
from cbr_custom_news_feeds.config.Custom_News__Shared_Constants                             import S3_FILE_NAME__RAW__FEED_XML, S3_FILE_NAME__RAW__FEED_DATA
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.routes.Routes__Hacker_News  import ROUTE_PATH__HACKER_NEWS
from tests.integration.news_feeds__objs_for_tests                                           import news_feeds__fast_api__app
from tests.qa.test__live_lambda_function                                                    import obj


class test__http__Routes__Hacker_News(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fast_api_server = Fast_API_Server(app=news_feeds__fast_api__app)
        cls.fast_api_server.start()
        assert cls.fast_api_server.is_port_open() is True

    @classmethod
    def tearDownClass(cls):
        cls.fast_api_server.stop()
        assert cls.fast_api_server.is_port_open() is False

    def test__files_paths(self):
        path = 'files-paths'
        response     = self.fast_api_server.requests_get(f'/{ROUTE_PATH__HACKER_NEWS}/{path}')
        response_obj = obj(response.json())
        assert response.status_code == 200
        assert response_obj.status  == 'ok'
        assert response_obj.data.latest_feed_xml .endswith(f'{S3_FILE_NAME__RAW__FEED_XML }.json')
        assert response_obj.data.latest_feed_data.endswith(f'{S3_FILE_NAME__RAW__FEED_DATA}.json')
