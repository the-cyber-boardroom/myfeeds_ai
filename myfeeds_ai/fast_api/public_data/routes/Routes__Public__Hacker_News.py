from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files import Hacker_News__Files

ROUTES__TAG__PUBLIC__HACKER_NEWS   = 'hacker-news'
ROUTES__PATHS__PUBLIC__HACKER_NEWS = [f'/{ROUTES__TAG__PUBLIC__HACKER_NEWS}/ping']

class Routes__Public__Hacker_News(Fast_API_Routes):
    tag  : str                = ROUTES__TAG__PUBLIC__HACKER_NEWS
    files: Hacker_News__Files

    def latest__feed_data(self):
        data_feed = self.files.feed_data__current()
        if data_feed:
            return data_feed.json()
        return {}

    def ping(self):
        return 'pong'

    def setup_routes(self):
        self.add_route_get(self.ping             )
        self.router.add_api_route(path='/latest/feed-data.json', endpoint=self.latest__feed_data, methods=['GET'])

