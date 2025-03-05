from osbot_fast_api.api.Fast_API_Routes                                                         import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__All     import Hacker_News__File__Articles__All
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__New     import Hacker_News__File__Articles__New

ROUTE_PATH__HACKER_NEWS__ARTICLES = 'hacker-news-articles'

ROUTES_PATHS__HACKER_NEWS__ARTICLES = [f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/current-articles'            ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/delete-file-articles-all'    ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/delete-file-articles-current',
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/delete-file-articles-new'    ]


class Routes__Hacker_News__Articles(Fast_API_Routes):
    tag                 : str                = ROUTE_PATH__HACKER_NEWS__ARTICLES

    def current_articles(self):
        with Hacker_News__File__Articles__Current() as _:
            _.load()
            return _.group_by_next_step()

    # def current_articles_exists(self):
    #     with Hacker_News__File__Current_Articles() as _:
    #         return _.exists__latest()

    def delete_file_articles_all(self):
        with Hacker_News__File__Articles__All() as _:
            return _.delete__latest()

    def delete_file_articles_current(self):
        with Hacker_News__File__Articles__Current() as _:
            return _.delete__latest()

    def delete_file_articles_new(self):
        with Hacker_News__File__Articles__New() as _:
            return _.delete__latest()

    def setup_routes(self):
        self.add_route_get   (self.current_articles             )
        self.add_route_delete(self.delete_file_articles_all     )
        self.add_route_delete(self.delete_file_articles_current )
        self.add_route_delete(self.delete_file_articles_new     )
