from fastapi                                                                    import Response
from osbot_fast_api.api.Fast_API_Routes                                         import Fast_API_Routes
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.owasp.actions.Owasp__Files__Top_10     import Owasp__Files__Top_10
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__File__Top_10        import Owasp__File__Top_10
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category  import Owasp__Top_10__Category

ROUTE_PATH__OWASP = 'owasp'

ROUTES_PATHS__OWASP = [f'/{ROUTE_PATH__OWASP}/all-files'   ,
                       f'/{ROUTE_PATH__OWASP}/raw-markdown']

class Routes__Owasp(Fast_API_Routes):
    tag                : str = ROUTE_PATH__OWASP
    owasp_files_top_10 : Owasp__Files__Top_10

    def raw_markdown(self, category: Owasp__Top_10__Category):
        file__category = self.owasp_files_top_10.file__category(category)
        markdown       = file__category.data()
        return Response(content=markdown, media_type=str(S3_Key__File__Content_Type.MARKDOWN))

    def all_files(self):
        storage = Owasp__File__Top_10().hacker_news_storage
        return storage.s3_db.s3_folder_files__all('public-data/owasp')

    def setup_routes(self):
        self.add_route_get(self.raw_markdown)
        self.add_route_get(self.all_files   )
