from unittest                                                                               import TestCase
from cbr_custom_data_feeds.fast_api.Data_Feeds__Fast_API                                    import Data_Feeds__Fast_API
from cbr_custom_data_feeds.fast_api.routes.Routes__Info                                     import ROUTES_PATHS__INFO
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.routes.Routes__Hacker_News  import ROUTES_PATHS__HACKER_NEWS
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.routes.Routes__OSS import ROUTES_PATHS__OSS
from tests.integration.data_feeds__objs_for_tests                                           import cbr_website__assert_local_stack


class test_Data_Feeds__Fast_API(TestCase):

    def setUp(self):
        cbr_website__assert_local_stack()
        self.fast_api = Data_Feeds__Fast_API()

    def test_base_path(self):
        assert self.fast_api.base_path == '/'
        assert self.fast_api.enable_cors is True

    def test_setup_routes(self):
        self.fast_api.setup()
        routes = self.fast_api.routes_paths()

        assert routes == sorted(['/',
                                 '/static'                                              ,
                                 '/config/info', '/config/status', '/config/version']  \
                                 + ROUTES_PATHS__INFO                                  \
                                 + ROUTES_PATHS__HACKER_NEWS                           \
                                 + ROUTES_PATHS__OSS                                   )



