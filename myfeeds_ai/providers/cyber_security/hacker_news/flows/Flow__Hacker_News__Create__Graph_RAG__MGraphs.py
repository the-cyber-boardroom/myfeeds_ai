# from typing                                                                                        import Dict, List
# from mgraph_db.providers.graph_rag.actions.Graph_RAG__Create_MGraph                                import Graph_RAG__Create_MGraph
# from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity                               import Schema__Graph_RAG__Entity
# from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                           import S3_Key__File_Extension
# from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB                            import S3_FILE_NAME__ARTICLE__TEXT_ENTITIES, S3_FILE_NAME__ARTICLE__GRAPH_ENTITIES
# from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                     import Hacker_News__Data
# from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Edit                     import Hacker_News__Edit
# from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article         import Hacker_News__Storage__Article
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                 import Schema__Feed__Article
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status         import Schema__Feed__Article__Status
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step           import Schema__Feed__Article__Step
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles                import Schema__Feed__Articles
# from osbot_utils.helpers.Obj_Id                                                                    import Obj_Id
# from osbot_utils.helpers.flows.Flow                                                                import Flow
# from osbot_utils.helpers.flows.decorators.flow                                                     import flow
# from osbot_utils.helpers.flows.decorators.task                                                     import task
# from osbot_utils.type_safe.Type_Safe                                                               import Type_Safe
#
# MAX_FILES_PROCESSED = 1
#
# class Flow__Hacker_News__Create__Graph_RAG__MGraphs(Type_Safe):
#     hacker_news_data        : Hacker_News__Data
#     hacker_news_edit        : Hacker_News__Edit
#     current_articles        : Schema__Feed__Articles
#     articles_to_process     : Dict[Obj_Id, Schema__Feed__Article]
#     create_graph_rag_mgraph : Graph_RAG__Create_MGraph
#     result__processed_files : List
#
#
#     @task()
#     def find_target_articles(self):
#         with self.hacker_news_data as _:
#             self.current_articles = _.current_articles()
#             for article_id, article in self.current_articles.articles.items():
#                 if article.next_step == Schema__Feed__Article__Step.STEP__3__CREATE_GRAPH:
#                     self.articles_to_process[article_id]=article
#             print(f"There are {len(self.articles_to_process)} articles to process")
#
#     @task()
#     def create_mgraphs(self):
#         for i, (article_id, article) in enumerate(self.articles_to_process.items()):
#             if i >= MAX_FILES_PROCESSED:
#                 break
#             article_storage = Hacker_News__Storage__Article(article_id=article_id)
#             location        = article.path__folder__source
#             #pprint(article_storage.files_in__path(location, include_sub_folders=True))
#             file_entities =  article_storage.load_from__path(path      = location                             ,
#                                                              file_id   = S3_FILE_NAME__ARTICLE__TEXT_ENTITIES ,
#                                                              extension = S3_Key__File_Extension.JSON          )
#
#             entities__description = file_entities.get('entities__description').get('entities')
#             entities__title       = file_entities.get('entities__title'      ).get('entities')
#
#             entities = []
#             for entity_data  in entities__title:
#                 if entity_data.get('node_data'):
#                     entity_data = entity_data.get('node_data')
#                     platform = entity_data.get('ecosystem',{}).get('platform')
#                     if type(platform) is str:
#                         entity_data['ecosystem']['platforms'] = [platform]
#                 entity        = Schema__Graph_RAG__Entity.from_json(entity_data)
#                 entities.append(entity)
#
#             entity_mgraph       = self.create_graph_rag_mgraph.from_entities       (entities)
#             entity_mgraph_bytes = self.create_graph_rag_mgraph.export_mgraph_to_png(entity_mgraph)
#
#
#             path_entities_mgraph_json = article_storage.save_to__path(data      = entity_mgraph.json__compress()      ,
#                                                                      path      = location                             ,
#                                                                      file_id   = S3_FILE_NAME__ARTICLE__GRAPH_ENTITIES,
#                                                                      extension = S3_Key__File_Extension.MGRAPH__JSON  )
#
#             content_type__png = "image/png"
#             path_entities_mgraph_png = article_storage.save_to__path(data        = entity_mgraph_bytes                  ,
#                                                                      path        = location                             ,
#                                                                      file_id     = S3_FILE_NAME__ARTICLE__GRAPH_ENTITIES,
#                                                                      extension    = S3_Key__File_Extension.MGRAPH__PNG   ,
#                                                                      content_type = content_type__png)
#             article.status = Schema__Feed__Article__Status.TO_MERGE_GRAPH
#             article.path__entity_mgraph__json = path_entities_mgraph_json
#             article.path_entities_mgraph_png  = path_entities_mgraph_png
#
#             result__processed_file = dict( entities                  = len(entities)                  ,
#                                            mgraph_stats              = entity_mgraph.data().stats()   ,
#                                            png_sizew                 = len(entity_mgraph_bytes)       ,
#                                            path_entities_mgraph_json = path_entities_mgraph_json      ,
#                                            path_entities_mgraph_png  = path_entities_mgraph_png       ,
#                                            article                    = article                       ,
#                                            article_id                = article_id                     ,
#                                            save_result = self.hacker_news_edit.save__current_articles(self.current_articles),
#                                            current_articles = self.current_articles)
#
#             self.result__processed_files.append(result__processed_file)
#
#         self.hacker_news_edit.save__current_articles(self.current_articles)
#
#     @flow()
#     def create_graph_rag_for_articles(self) -> Flow:
#         self.find_target_articles   ()
#         self.create_mgraphs()
#         return self.result__processed_files
#
#
#     def run(self):
#         return self.create_graph_rag_for_articles().execute_flow()