from osbot_fast_api.api.Fast_API_Routes                                                     import Fast_API_Routes
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Files         import OSS__Files
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Http_Content  import OSS__Http_Content

ROUTE_PATH__OSS   = 'open-security-summit'
ROUTES_PATHS__OSS = [ f'/{ROUTE_PATH__OSS}/raw-data'   ,
                      f'/{ROUTE_PATH__OSS}/all-files'  ]


class Routes__OSS(Fast_API_Routes):
    tag         : str                       = ROUTE_PATH__OSS
    http_content: OSS__Http_Content
    files       : OSS__Files

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.files.s3_db.setup()            # todo: refactor this to a better place (we need this to make sure the db is setup, and the s3 bucket created)

    def all_files(self):
        return self.files.all_files()

    def raw_data(self):
        return self.files.raw_content__current().json()

    def setup_routes(self):
        self.add_route_get(self.all_files)
        self.add_route_get(self.raw_data )