from fastapi                                                                                    import Response
from osbot_fast_api.api.Fast_API_Routes                                                         import Fast_API_Routes
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                  import Hacker_News__Data
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data__Digest          import Hacker_News__Data__Digest
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step        import Schema__Feed__Article__Step
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id

ROUTE_PATH__HACKER_NEWS__ARTICLES   = 'hacker-news-articles'

ROUTES_PATHS__HACKER_NEWS__ARTICLES = [f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/digest-articles'                 ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/digest-articles-data'            ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/digest-articles-html-page'       ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/digest-articles-html-section'    ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/new-articles'                    ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/current-articles'                ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/current-article'                 ]
                                       #f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/current-article-change-next-step']
                                       # f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/delete-file-articles-all'        ,
                                       # f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/delete-file-articles-current'    ,
                                       # f'/{ROUTE_PATH__HACKER_NEWS__ARTICLES}/delete-file-articles-new'        ]


class Routes__Hacker_News__Articles(Fast_API_Routes):
    tag                     : str                = ROUTE_PATH__HACKER_NEWS__ARTICLES
    hacker_news_data        : Hacker_News__Data
    hacker_news_data_digest : Hacker_News__Data__Digest

    def digest_articles(self):
        return self.hacker_news_data_digest.digest_articles()

    def digest_articles_data(self):
        return self.hacker_news_data_digest.digest_articles__view_data()

    def digest_articles_html_page(self):
        content      = self.hacker_news_data_digest.digest_articles__html__as_page()
        return Response(content=content, media_type=str(S3_Key__File__Content_Type.HTML))

    def digest_articles_html_section(self):
        content      = self.hacker_news_data_digest.digest_articles__html__as_section()
        return Response(content=content, media_type=str(S3_Key__File__Content_Type.HTML))

    def new_articles(self):
        return self.hacker_news_data.new_articles().json()

    def current_articles(self):
        with Hacker_News__File__Articles__Current() as _:
            _.load()
            return _.group_by_next_step()

    def current_article(self, article_id: str):
        article_id = Obj_Id(article_id)                 # todo: add native support to OSBot_Fast_API for using Type_Safe transparently on these routes methods
        with Hacker_News__File__Articles__Current() as _:
            _.load()
            return _.article(article_id)

    # def current_article_change_next_step(self, article_id: str, next_step: Schema__Feed__Article__Step):
    #     article_id = Obj_Id(article_id)
    #     with Hacker_News__File__Articles__Current() as _:
    #         _.load()
    #         return _.change_article_next_step(article_id, next_step)

    # def current_articles_exists(self):
    #     with Hacker_News__File__Current_Articles() as _:
    #         return _.exists__latest()

    # def delete_file_articles_all(self):
    #     with Hacker_News__File__Articles__All() as _:
    #         return _.delete__latest()
    #
    # def delete_file_articles_current(self):
    #     with Hacker_News__File__Articles__Current() as _:
    #         return _.delete__latest()
    #
    # def delete_file_articles_new(self):
    #     with Hacker_News__File__Articles__New() as _:
    #         return _.delete__latest()

    def setup_routes(self):
        self.add_route_get   (self.digest_articles                  )
        self.add_route_get   (self.digest_articles_data             )
        self.add_route_get   (self.digest_articles_html_page        )
        self.add_route_get   (self.digest_articles_html_section     )
        self.add_route_get   (self.new_articles                     )
        self.add_route_get   (self.current_articles                 )
        self.add_route_get   (self.current_article                  )
        #self.add_route_get   (self.current_article_change_next_step )
        # self.add_route_delete(self.delete_file_articles_all         )
        # self.add_route_delete(self.delete_file_articles_current     )
        # self.add_route_delete(self.delete_file_articles_new         )
