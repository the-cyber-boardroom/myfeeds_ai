import myfeeds_ai
from myfeeds_ai.providers.models.Model__RSS_Providers   import Model__RSS_Providers
from osbot_utils.utils.Toml                             import toml_load
from osbot_utils.utils.Files                            import path_combine_safe
from osbot_utils.type_safe.Type_Safe                     import Type_Safe

FILE_NAME__RSS_PROVIDERS_DATA = 'providers/rss-providers-data.toml'

class RSS_Providers(Type_Safe):

    def data(self):
        raw_data = toml_load(self.path_rss_providers_data())
        return Model__RSS_Providers.from_json(raw_data)

    def path_rss_providers_data(self):
        return path_combine_safe(myfeeds_ai.path, FILE_NAME__RSS_PROVIDERS_DATA)