from unittest                                           import TestCase
from osbot_utils.utils.Misc                             import list_set
from osbot_utils.utils.Toml                             import toml_load
from osbot_utils.utils.Files                            import file_exists
from myfeeds_ai.providers.models.Model__RSS_Providers   import Model__RSS_Providers
from myfeeds_ai.providers.RSS_Providers                 import RSS_Providers, FILE_NAME__RSS_PROVIDERS_DATA

class test_RSS_Providers(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rss_providers = RSS_Providers()

    def test_data(self):
        with self.rss_providers as _:
            data = _.data()
            assert type(data)               is Model__RSS_Providers
            assert data.json()              == toml_load(_.path_rss_providers_data())
            assert list_set(data.providers) == ['cso-online', 'hacker-news']

    def test_path_rss_providers_data(self):
        with self.rss_providers as _:
            path = _.path_rss_providers_data()
            assert FILE_NAME__RSS_PROVIDERS_DATA in path
            assert file_exists(path)

