from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                  import Model__Data_Feeds__Providers
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.files.Website__Files import Website__Files
from myfeeds_ai.shared.http.Http__Request__Execute__Requests                    import Http__Request__Execute__Requests
from myfeeds_ai.shared.http.schemas.Schema__Http__Action                        import Schema__Http__Action
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Methods              import Schema__Http__Request__Methods
from osbot_utils.helpers.duration.decorators.print_duration import print_duration
from osbot_utils.helpers.safe_str.Safe_Str__Url                                 import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.utils.Http import url_join_safe

URL__DOCS_DINISCRUZ_AI = Safe_Str__Url("https://docs.diniscruz.ai/")

class Docs_DinisCruz_Ai__Files(Type_Safe):
    base_url             : Safe_Str__Url
    http_request_execute : Http__Request__Execute__Requests
    provider_name        : Model__Data_Feeds__Providers
    website_files        : Website__Files

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url      = URL__DOCS_DINISCRUZ_AI
        self.provider_name = Model__Data_Feeds__Providers.DOCS_DINISCRUZ_AI
        self.website_files = Website__Files(provider_name=self.provider_name)

    def file__home_page(self):
        return self.website_files.file__home_page()

    def all_files(self):
        return self.website_files.website_storage.s3_db.provider__all_files()
        # all_files = storage.s3_db.s3_folder_files__all(f'public-data/{self.provider_name}')
        # return sorted(all_files)

    def home_page__data(self) -> str:
        file = self.file__home_page()
        if file.exists():
            return file.data()
        http_action = self.get__path('/')
        file.save_data(http_action)
        return http_action

    def get__path(self, path='/') -> Schema__Http__Action:
        with self.http_request_execute as _:
            url         = Safe_Str__Url(url_join_safe(self.base_url, path))         # todo: add a variation of the method url_join_safe that returns an Safe_Str__Url object
            http_action = _.execute__get(url=url)
            return http_action
            #response    = http_action.response