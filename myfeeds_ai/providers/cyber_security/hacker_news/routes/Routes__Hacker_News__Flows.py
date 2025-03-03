from osbot_fast_api.api.Fast_API_Routes                                         import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Flows import Hacker_News__Flows
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__1__Download_RSS_Feed import \
    Flow__Hacker_News__1__Download_RSS_Feed
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__2__Create_Articles_Timeline import \
    Flow__Hacker_News__2__Create_Articles_Timeline

ROUTE_PATH__HACKER_NEWS__FLOWS = 'hacker-news-flows'

ROUTES_PATHS__HACKER_NEWS__FLOWS = [f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/current-articles'                ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-1-download-rss-feed'        ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-2-create-articles-timeline' ]

class Routes__Hacker_News__Flows(Fast_API_Routes):
    tag                 : str                = 'hacker-news-flows'
    hacker_news__flows  : Hacker_News__Flows

    def current_articles(self):
        return self.hacker_news__flows.current_articles__group_by__status()

    def flow_1_download_rss_feed(self):
        return Flow__Hacker_News__1__Download_RSS_Feed().run().flow_return_value

    def flow_2_create_articles_timeline(self):
        return Flow__Hacker_News__2__Create_Articles_Timeline().run().flow_output()

    def setup_routes(self):
        self.add_route_get(self.current_articles               )
        self.add_route_get(self.flow_1_download_rss_feed       )
        self.add_route_get(self.flow_2_create_articles_timeline)