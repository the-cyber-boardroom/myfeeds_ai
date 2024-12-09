from unittest                                           import TestCase
from cbr_custom_data_feeds.fast_api.routes.Routes__Info import Routes__Info
from cbr_custom_data_feeds.utils.Version                import version__cbr_custom_data_feeds


class test__int__Routes__UK(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_data_feeds = Routes__Info()

    def test_routes_setup(self):
        with self.routes_data_feeds as _:
            assert _.tag == 'info'
            _.setup_routes()
            assert '/version' in _.routes_paths()

    def test__version(self):
        with self.routes_data_feeds as _:
            assert _.version() == { 'version': version__cbr_custom_data_feeds }
