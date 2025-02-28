from osbot_fast_api.api.Fast_API_Routes                                         import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Flows import Hacker_News__Flows

ROUTE_PATH__HACKER_NEWS__FLOWS = 'hacker-news-flows'

ROUTES_PATHS__HACKER_NEWS__FLOWS = [f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/current-articles' ]

class Routes__Hacker_News__Flows(Fast_API_Routes):
    tag                 : str                = 'hacker-news-flows'
    hacker_news__flows  : Hacker_News__Flows

    def current_articles(self):
        return self.hacker_news__flows.current_articles__group_by__status()


    def setup_routes(self):
        self.add_route_get(self.current_articles      )