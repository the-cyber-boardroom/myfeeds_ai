from osbot_fast_api.api.Fast_API_Routes                                                                                         import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Flows                                                 import Hacker_News__Flows
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_MGraphs import Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_MGraphs
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View import \
    Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__1__Download_RSS_Feed                              import Flow__Hacker_News__1__Download_RSS_Feed
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__2__Create_Articles_Timeline                       import Flow__Hacker_News__2__Create_Articles_Timeline
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__3__Extract_New_Articles                           import Flow__Hacker_News__3__Extract_New_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__4__Article__Step_1__Create_Article_Files          import Flow__Hacker_News__4__Article__Step_1__Create_Article_Files
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__5__Article__Step_2__Create_Article_Markdown       import Flow__Hacker_News__5__Article__Step_2__Create_Article_Markdown
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Entities          import Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__7__Article__Step_4__Create_Text_Entities_Graphs   import Flow__Hacker_News__7__Article__Step_4__Create_Text_Entities_Graphs
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs    import Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs     import Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs

ROUTE_PATH__HACKER_NEWS__FLOWS = 'hacker-news-flows'

ROUTES_PATHS__HACKER_NEWS__FLOWS = [f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-1-download-rss-feed'                           ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-2-create-articles-timeline'                    ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-3-flow-extract-new-articles'                   ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-4-article-step-1-create-article-files'         ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-5-article-step-2-create-article-markdown'      ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-6-article-step-3-llm-text-to-entities'         ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-7-article-step-4-create-text-entities-graphs'  ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-8-article-step-5-merge-text-entities-graphs'   ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-9-article-step-6-merge-day-entities-graphs'    ,
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-10-article-step-7-create-feed-entities-mgraphs',
                                    f'/{ROUTE_PATH__HACKER_NEWS__FLOWS}/flow-11-article-step-8-create-entities-tree-view'   ]


class Routes__Hacker_News__Flows(Fast_API_Routes):
    tag                 : str                = ROUTE_PATH__HACKER_NEWS__FLOWS
    hacker_news__flows  : Hacker_News__Flows

    def flow_1_download_rss_feed(self):
        return Flow__Hacker_News__1__Download_RSS_Feed().run().flow_return_value

    def flow_2_create_articles_timeline(self):
        return Flow__Hacker_News__2__Create_Articles_Timeline().run().flow_output()

    def flow_3_flow_extract_new_articles(self, current__path:str ='2025/03/01/00'):
        return Flow__Hacker_News__3__Extract_New_Articles(current__path=current__path).run().flow_output()

    def flow_4_article_step_1_create_article_files(self, max_articles_to_save:int = 1):
        return Flow__Hacker_News__4__Article__Step_1__Create_Article_Files(max_articles_to_save=max_articles_to_save).run().flow_output()

    def flow_5_article_step_2_create_article_markdown(self):
        return Flow__Hacker_News__5__Article__Step_2__Create_Article_Markdown().run().flow_output()

    def flow_6_article_step_3_llm_text_to_entities(self, max_articles_to_create:int = 1):
        return Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Entities(max_articles_to_create=max_articles_to_create).run().flow_output()

    def flow_7_article_step_4_create_text_entities_graphs(self, max_graphs_to_create: int=1):
        return Flow__Hacker_News__7__Article__Step_4__Create_Text_Entities_Graphs(max_graphs_to_create=max_graphs_to_create).run().flow_output()

    def flow_8_article_step_5_merge_text_entities_graphs(self,max_graphs_to_merge: int=1):
        return Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs(max_graphs_to_merge=max_graphs_to_merge).run().flow_output()

    def flow_9_article_step_6_merge_day_entities_graphs(self, max_graphs_to_merge:int=1):
        return Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs(max_graphs_to_merge=max_graphs_to_merge).run().flow_output()

    def flow_10_article_step_7_create_feed_entities_mgraphs(self, max_articles_to_move: int = 1):
        return Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_MGraphs(max_articles_to_move=max_articles_to_move).run().flow_output()

    def flow_11_article_step_8_create_entities_tree_view(self,max_articles_to_move: int = 1):
        return Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View(max_articles_to_move=max_articles_to_move).run().flow_output()

    def setup_routes(self):
        self.add_route_get(self.flow_1_download_rss_feed                           )
        self.add_route_get(self.flow_2_create_articles_timeline                    )
        self.add_route_get(self.flow_3_flow_extract_new_articles                   )
        self.add_route_get(self.flow_4_article_step_1_create_article_files         )
        self.add_route_get(self.flow_5_article_step_2_create_article_markdown      )
        self.add_route_get(self.flow_6_article_step_3_llm_text_to_entities         )
        self.add_route_get(self.flow_7_article_step_4_create_text_entities_graphs  )
        self.add_route_get(self.flow_8_article_step_5_merge_text_entities_graphs   )
        self.add_route_get(self.flow_9_article_step_6_merge_day_entities_graphs    )
        self.add_route_get(self.flow_10_article_step_7_create_feed_entities_mgraphs)
        self.add_route_get(self.flow_11_article_step_8_create_entities_tree_view   )