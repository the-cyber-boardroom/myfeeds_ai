from osbot_fast_api.api.Fast_API                    import Fast_API
from myfeeds_ai.rss_feeds.routes.Routes__RSS_Parser import Routes__RSS_Parser


class RSS_Feeds__Fast_API(Fast_API):
    base_path : str =  '/rss-feeds'

    def setup_routes(self):
        self.add_routes(Routes__RSS_Parser)
        return self