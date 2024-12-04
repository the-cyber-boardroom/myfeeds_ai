from osbot_fast_api.api.Fast_API_Routes                                                   import Fast_API_Routes
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Http_Content import Hacker_News__Http_Content

ROUTES_PATHS__HACKER_NEWS = [ '/hacker-news/feed']


class Routes__Hacker_News(Fast_API_Routes):
    tag: str = 'hacker-news'
    http_content: Hacker_News__Http_Content

    def feed(self):                                         # Get the complete feed data
        return self.http_content.get_feed_data()


    def setup_routes(self):
        self.add_route_get(self.feed)
