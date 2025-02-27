from unittest                                           import TestCase
from myfeeds_ai.fast_api.routes.Routes__Info import Routes__Info
from myfeeds_ai.utils.Version                import version__myfeeds_ai


class test_Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_info = Routes__Info()

    def test_version(self):
        assert self.routes_info.version() == {'version': version__myfeeds_ai}

    def test_setup_routes(self):
        with self.routes_info as _:
            assert _.routes_paths() == []
            _.setup_routes()
            assert _.routes_paths() == ['/version']