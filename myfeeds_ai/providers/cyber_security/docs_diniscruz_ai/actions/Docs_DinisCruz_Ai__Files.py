from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                  import Model__Data_Feeds__Providers
from myfeeds_ai.mgraphs.html_to_mgraph.Html_Document__To__Html_MGraph           import Html_Document__To__Html_MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_Document__To__Html_MGraph__Schema   import Html_Document__To__Html_MGraph__Schema
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph                              import Html_MGraph
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.files.Website__Files import Website__Files
from myfeeds_ai.shared.http.Http__Request__Execute__Requests                    import Http__Request__Execute__Requests
from myfeeds_ai.shared.http.schemas.Schema__Http__Action                        import Schema__Http__Action
from osbot_utils.helpers.html.Html_Dict__To__Html_Document                      import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.Html__To__Html_Dict                               import Html__To__Html_Dict
from osbot_utils.helpers.html.schemas.Schema__Html_Document                     import Schema__Html_Document
from osbot_utils.helpers.safe_str.Safe_Str__Url                                 import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.utils.Http                                                     import url_join_safe

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

    def file__home_page__mgraph(self):
        return self.website_files.file__home_page__mgraph()

    def all_files(self):
        return self.website_files.website_storage.s3_db.provider__all_files()

    def home_page__data(self) -> Schema__Http__Action:
        file = self.file__home_page()
        if file.exists():
            return file.data()
        http_action = self.get__path('/')
        file.save_data(http_action)
        return http_action

    def home_page__html(self) -> str:
        return self.home_page__data().response.text

    def home_page__html_dict(self) -> dict:
        html = self.home_page__data().response.text
        html_dict = Html__To__Html_Dict(html=html).convert()
        return html_dict

    def home_page__html_document(self) -> Schema__Html_Document:
        html          = self.home_page__data().response.text
        html_dict     = Html__To__Html_Dict         (html       = html     ).convert()
        html_document = Html_Dict__To__Html_Document(html__dict = html_dict).convert()
        return html_document

    def home_page__html_mgraph(self) -> Html_MGraph:
        file = self.file__home_page__mgraph()
        if file.exists():
            return file.data()
        html_document = self.home_page__html_document()
        html_mgraph   = Html_Document__To__Html_MGraph(html_document=html_document).convert()
        file.save_data(html_mgraph)
        return html_mgraph

    def home_page__html_mgraph__schema(self, target_file=None):
        html_document = self.home_page__html_document()
        with Html_Document__To__Html_MGraph__Schema(html_document=html_document) as _:
            _.convert()
            png_bytes = _.screenshot(target_file=target_file)
            return png_bytes




    def get__path(self, path='/') -> Schema__Http__Action:
        with self.http_request_execute as _:
            url         = Safe_Str__Url(url_join_safe(self.base_url, path))         # todo: add a variation of the method url_join_safe that returns an Safe_Str__Url object
            http_action = _.execute__get(url=url)
            return http_action