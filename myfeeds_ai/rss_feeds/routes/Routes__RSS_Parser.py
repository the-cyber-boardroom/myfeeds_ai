from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from myfeeds_ai.providers.RSS_Providers import RSS_Providers
from myfeeds_ai.rss_feeds.RSS_Feeds     import RSS_Feeds

DEFAULT__FEED_URL = 'https://feeds.feedburner.com/TheHackersNews'

class Routes__RSS_Parser(Fast_API_Routes):
    tag          : str = 'rss-parser'
    rss_feeds    : RSS_Feeds
    rss_providers: RSS_Providers


    def providers(self):
        return self.rss_providers.data()

    def url_to_xml(self, feed_url=DEFAULT__FEED_URL):
        return self.rss_feeds.feed_url__to__xml(feed_url)

    def url_to_xml_file(self, feed_url=DEFAULT__FEED_URL):
        return self.rss_feeds.feed_url__to__xml_file(feed_url).json()

    def url_to_xml_json(self, feed_url=DEFAULT__FEED_URL):
        return self.rss_feeds.feed_url__to__json(feed_url)

    def url_to_rss_json(self, feed_url=DEFAULT__FEED_URL):
        return self.rss_feeds.feed_url__to__rss_feed(feed_url).json()

    def setup_routes(self):
        self.add_route_get(self.providers      )
        self.add_route_get(self.url_to_xml     )
        self.add_route_get(self.url_to_xml_file)
        self.add_route_get(self.url_to_xml_json)
        self.add_route_get(self.url_to_rss_json)