import cbr_custom_data_feeds
from osbot_fast_api.api.Fast_API                                                            import Fast_API
from osbot_utils.utils.Files                                                                import path_combine
from cbr_custom_data_feeds.fast_api.routes.Routes__Info                                     import Routes__Info
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.routes.Routes__OSS import Routes__OSS
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.routes.Routes__Hacker_News  import Routes__Hacker_News



class Data_Feeds__Fast_API(Fast_API):
    base_path  : str  = '/'
    enable_cors: bool = True

    def setup_routes(self):
        self.add_routes(Routes__Info)
        self.add_routes(Routes__Hacker_News)
        self.add_routes(Routes__OSS        )

    def path_static_folder(self):
        return path_combine(cbr_custom_data_feeds.path, 'static')
