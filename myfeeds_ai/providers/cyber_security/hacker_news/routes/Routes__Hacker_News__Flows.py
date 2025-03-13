from osbot_fast_api.api.Fast_API_Routes                                                                     import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Flows                             import Hacker_News__Flows
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__1__Download_RSS_Feed          import Flow__Hacker_News__1__Download_RSS_Feed
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__2__Create_Articles_Timeline   import Flow__Hacker_News__2__Create_Articles_Timeline
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__3__Extract_New_Articles       import Flow__Hacker_News__3__Extract_New_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__4__Create_Article_Files       import Flow__Hacker_News__4__Create_Article_Files
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__5__Create_Article_Markdown    import Flow__Hacker_News__5__Create_Article_Markdown

ROUTE_PATH__HACKER_NEWS__FLOWS = 'hacker-news-flows'

ROUTES_PATHS__HACKER_NEWS__FLOWS = [f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-1-download-rss-feed'         ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-2-create-articles-timeline'  ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-3-flow-extract-new-articles' ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-4-create-article-files'      ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-5-create-article-markdown'   ]


class Routes__Hacker_News__Flows(Fast_API_Routes):
    tag                 : str                = ROUTE_PATH__HACKER_NEWS__FLOWS
    hacker_news__flows  : Hacker_News__Flows

    def flow_1_download_rss_feed(self):
        return Flow__Hacker_News__1__Download_RSS_Feed().run().flow_return_value

    def flow_2_create_articles_timeline(self):
        return Flow__Hacker_News__2__Create_Articles_Timeline().run().flow_output()

    def flow_3_flow_extract_new_articles(self, current__path:str ='2025/03/01/00'):
        return Flow__Hacker_News__3__Extract_New_Articles(current__path=current__path).run().flow_output()

    def flow_4_create_article_files(self):
        return Flow__Hacker_News__4__Create_Article_Files().run().flow_output()

    def flow_5_create_article_markdown(self):
        return Flow__Hacker_News__5__Create_Article_Markdown().run().flow_output()


    def setup_routes(self):
        self.add_route_get(self.flow_1_download_rss_feed        )
        self.add_route_get(self.flow_2_create_articles_timeline )
        self.add_route_get(self.flow_3_flow_extract_new_articles)
        self.add_route_get(self.flow_4_create_article_files     )
        self.add_route_get(self.flow_5_create_article_markdown  )