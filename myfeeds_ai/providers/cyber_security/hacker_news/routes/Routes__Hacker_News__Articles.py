from osbot_fast_api.api.Fast_API_Routes                                                         import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Current_Articles  import Hacker_News__File__Current_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__New_Articles import \
    Hacker_News__File__New_Articles

ROUTE_PATH__HACKER_NEWS__ARTICLES = 'hacker-news-articles'

ROUTES_PATHS__HACKER_NEWS__ARTICLES = [f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/current-articles'       ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/current-articles-delete',
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/new-articles-delete'    ]


class Routes__Hacker_News__Articles(Fast_API_Routes):
    tag                 : str                = ROUTE_PATH__HACKER_NEWS__ARTICLES

    def current_articles(self):
        with Hacker_News__File__Current_Articles() as _:
            _.load()
            return _.group_by_next_step()

    # def current_articles_exists(self):
    #     with Hacker_News__File__Current_Articles() as _:
    #         return _.exists__latest()

    def current_articles_delete(self):
        with Hacker_News__File__Current_Articles() as _:
            return _.delete__latest()

    def new_articles_delete(self):
        with Hacker_News__File__New_Articles() as _:
            return _.delete__latest()

    def setup_routes(self):
        self.add_route_get   (self.current_articles       )
        # self.add_route_post  (self.current_articles_exists)
        self.add_route_delete(self.current_articles_delete)
        self.add_route_delete(self.new_articles_delete    )
