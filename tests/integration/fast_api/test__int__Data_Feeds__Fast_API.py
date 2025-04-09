from unittest                                                                             import TestCase
from myfeeds_ai.fast_api.Data_Feeds__Fast_API                                             import Data_Feeds__Fast_API
from myfeeds_ai.fast_api.routes.Routes__Debug                                             import ROUTES__EXPECTED_PATHS__DEBUG
from myfeeds_ai.fast_api.routes.Routes__Info                                              import ROUTES_PATHS__INFO
from myfeeds_ai.personas.routes.Routes__My_Feeds__Personas                                import ROUTES_PATHS__MY_FEEDS__PERSONAS
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News           import ROUTES_PATHS__HACKER_NEWS
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News__Articles import ROUTES_PATHS__HACKER_NEWS__ARTICLES
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News__Cache    import ROUTES_PATHS__HACKER_NEWS__CACHE
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News__Flows    import ROUTES_PATHS__HACKER_NEWS__FLOWS
from myfeeds_ai.providers.cyber_security.open_security_summit.routes.Routes__OSS          import ROUTES_PATHS__OSS
from tests.integration.data_feeds__objs_for_tests                                         import myfeeds_tests__setup_local_stack

class test_Data_Feeds__Fast_API(TestCase):

    def setUp(self):
        myfeeds_tests__setup_local_stack()
        self.fast_api = Data_Feeds__Fast_API()

    def test_base_path(self):
        assert self.fast_api.base_path == '/'
        assert self.fast_api.enable_cors is True

    def test_setup_routes(self):
        self.fast_api.setup()
        routes = self.fast_api.routes_paths()

        assert routes == sorted(['/',
                                 '/static', '/ui'                                      ,
                                 '/config/info', '/config/status', '/config/version']  \
                                 + ROUTES_PATHS__INFO                                  \
                                 + ROUTES_PATHS__HACKER_NEWS                           \
                                 + ROUTES_PATHS__HACKER_NEWS__ARTICLES                 \
                                 + ROUTES_PATHS__HACKER_NEWS__FLOWS                    \
                                 + ROUTES_PATHS__MY_FEEDS__PERSONAS                    \
                                 + ROUTES_PATHS__HACKER_NEWS__CACHE                    \
                                 + ROUTES_PATHS__OSS                                   \
                                 + ROUTES__EXPECTED_PATHS__DEBUG                       )



