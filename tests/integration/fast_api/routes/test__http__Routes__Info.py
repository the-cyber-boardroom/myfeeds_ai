from unittest                                     import TestCase
from osbot_fast_api.utils.Fast_API_Server         import Fast_API_Server
from myfeeds_ai.utils.Version          import version__myfeeds_ai
from tests.integration.data_feeds__objs_for_tests import data_feeds__fast_api__app


class test__http__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fast_api_server = Fast_API_Server(app=data_feeds__fast_api__app)
        cls.fast_api_server.start()
        assert cls.fast_api_server.is_port_open() is True

    @classmethod
    def tearDownClass(cls):
        cls.fast_api_server.stop()
        assert cls.fast_api_server.is_port_open() is False

    def test__info__version(self):
        response = self.fast_api_server.requests_get('/info/version')
        assert response.status_code == 200
        assert response.json()      == {'version': version__myfeeds_ai }
