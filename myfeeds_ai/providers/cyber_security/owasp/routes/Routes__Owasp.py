from fastapi                                                                    import Response
from osbot_fast_api.api.Fast_API_Routes                                         import Fast_API_Routes
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.owasp.actions.Owasp__Files__Top_10     import Owasp__Files__Top_10
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__File__Top_10        import Owasp__File__Top_10
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category  import Owasp__Top_10__Category

ROUTE_PATH__OWASP = 'owasp'

ROUTES_PATHS__OWASP = [f'/{ROUTE_PATH__OWASP}/all-files'    ,
                       f'/{ROUTE_PATH__OWASP}/data-to-parse',
                       f'/{ROUTE_PATH__OWASP}/ontology'     ,
                       f'/{ROUTE_PATH__OWASP}/taxonomy'     ,
                       f'/{ROUTE_PATH__OWASP}/rdf-triples'  ,
                       f'/{ROUTE_PATH__OWASP}/screenshot'   ,
                       f'/{ROUTE_PATH__OWASP}/raw-data'     ,
                       f'/{ROUTE_PATH__OWASP}/raw-data-json']

class Routes__Owasp(Fast_API_Routes):
    tag                : str = ROUTE_PATH__OWASP
    owasp_files_top_10 : Owasp__Files__Top_10

    def data_to_parse(self, category: Owasp__Top_10__Category):
        data_to_parse = self.owasp_files_top_10.category__data_to_parse(category)
        return Response(content=data_to_parse, media_type=str(S3_Key__File__Content_Type.TXT))

    def ontology(self, category: Owasp__Top_10__Category):
        ontology = self.owasp_files_top_10.ontology(category)
        return ontology

    def taxonomy(self, category: Owasp__Top_10__Category):
        ontology = self.owasp_files_top_10.taxonomy(category)
        return ontology

    def rdf_triples(self, category: Owasp__Top_10__Category):
        rdf_triples = self.owasp_files_top_10.rdf_triples(category)
        return rdf_triples

    def screenshot(self, category: Owasp__Top_10__Category):
        png_bytes = self.owasp_files_top_10.screenshot(category)
        return Response(content=png_bytes, media_type=str(S3_Key__File__Content_Type.PNG))



    def raw_data(self, category: Owasp__Top_10__Category):
        raw_data = self.owasp_files_top_10.raw_data(category)
        return Response(content=raw_data, media_type=str(S3_Key__File__Content_Type.MARKDOWN))

    def raw_data_json(self, category: Owasp__Top_10__Category):
        raw_data_json = self.owasp_files_top_10.raw_data__json(category)
        return raw_data_json


    def all_files(self):
        storage   = Owasp__File__Top_10().hacker_news_storage
        all_files = storage.s3_db.s3_folder_files__all('public-data/owasp')
        return sorted(all_files)

    def setup_routes(self):
        self.add_route_get(self.data_to_parse   )
        self.add_route_get(self.ontology        )
        self.add_route_get(self.taxonomy        )
        self.add_route_get(self.rdf_triples     )
        self.add_route_get(self.screenshot      )
        self.add_route_get(self.raw_data        )
        self.add_route_get(self.raw_data_json   )
        self.add_route_get(self.all_files       )
