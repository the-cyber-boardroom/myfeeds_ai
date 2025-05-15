from fastapi                                                                                import Response
from osbot_fast_api.api.Fast_API_Routes                                                     import Fast_API_Routes
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.actions.Docs_DinisCruz_Ai__Files import Docs_DinisCruz_Ai__Files

ROUTE_PATH__DOCS_DINISCRUZ_AI   = 'docs-diniscruz-ai'
ROUTES_PATHS__DOCS_DINISCRUZ_AI = [f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/all-files'               ,
                                   f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/home-page-data'          ,
                                   f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/home-page-html'          ,
                                   f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/home-page-html-dict'     ,
                                   f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/home-page-html-document' ,
                                   f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/home-page-html-mgraph'   ,
                                   f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/home-page-html-schema'   ]

class Routes__Docs_DinisCruz_Ai(Fast_API_Routes):
    tag                      : str = ROUTE_PATH__DOCS_DINISCRUZ_AI
    files__docs_diniscruz_ai : Docs_DinisCruz_Ai__Files

    def all_files(self):
        return self.files__docs_diniscruz_ai.all_files()

    def home_page_data(self):
        return self.files__docs_diniscruz_ai.home_page__data()

    def home_page_html(self):
        content =  self.files__docs_diniscruz_ai.home_page__html()
        return Response(content=content, media_type=str(S3_Key__File__Content_Type.HTML))

    def home_page_html_dict(self):
        return self.files__docs_diniscruz_ai.home_page__html_dict()

    def home_page_html_document(self):
        return self.files__docs_diniscruz_ai.home_page__html_document()

    def home_page_html_mgraph(self):
        return self.files__docs_diniscruz_ai.home_page__html_mgraph().json__compress()

    def home_page_html_schema(self):
        png_bytes =  self.files__docs_diniscruz_ai.home_page__html_mgraph__schema()
        return Response(content=png_bytes, media_type=str(S3_Key__File__Content_Type.PNG))


    def setup_routes(self):
        self.add_route_get(self.all_files              )
        self.add_route_get(self.home_page_data         )
        self.add_route_get(self.home_page_html         )
        self.add_route_get(self.home_page_html_dict    )
        self.add_route_get(self.home_page_html_document)
        self.add_route_get(self.home_page_html_mgraph  )
        self.add_route_get(self.home_page_html_schema  )

