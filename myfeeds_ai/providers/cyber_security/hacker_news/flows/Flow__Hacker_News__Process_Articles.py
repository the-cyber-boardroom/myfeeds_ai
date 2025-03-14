# from typing                                                                                        import Dict
# from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                           import S3_Key__File_Extension
# from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB                            import S3_FILE_NAME__ARTICLE__FEED_ARTICLE, S3_FILE_NAME__ARTICLE__TEXT_ENTITIES
# from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                     import Hacker_News__Data
# from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Edit                     import Hacker_News__Edit
# from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage                  import Hacker_News__Storage
# from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article         import Hacker_News__Storage__Article
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                 import Schema__Feed__Article
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Entities       import Schema__Feed__Article__Entities, Schema__Feed__Text__Entities
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status         import Schema__Feed__Article__Status
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step           import Schema__Feed__Article__Step
# from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles                import Schema__Feed__Articles
# from osbot_utils.helpers.duration.decorators.capture_duration                                      import capture_duration
# from osbot_utils.helpers.Obj_Id                                                                    import Obj_Id
# from osbot_utils.helpers.flows.Flow                                                                import Flow
# from osbot_utils.helpers.flows.decorators.flow                                                     import flow
# from osbot_utils.helpers.flows.decorators.task                                                     import task
# from osbot_utils.type_safe.Type_Safe                                                               import Type_Safe
# from osbot_utils.utils.Env                                                                         import env_value
# from osbot_utils.utils.Lists                                                                       import list_index_by
#
# from osbot_utils.utils.Dev import pprint
#
# DEFAULT__MAX_ARTICLES_TO_PROCESS = 1
#
# class Flow__Hacker_News__Process_Articles(Type_Safe):
#     hacker_news_data            : Hacker_News__Data
#     hacker_news_edit            : Hacker_News__Edit
#     hacker_news_storage         : Hacker_News__Storage
#
#     current_articles            : Schema__Feed__Articles
#     articles_to_process         : Dict[Obj_Id,Schema__Feed__Article]
#     result__create_text_entities: dict
#
#     @task()
#     def load_new_articles(self):
#         self.current_articles = self.hacker_news_data.current_articles()
#         for article_id, article in self.current_articles.articles.items():
#             if article.status == Schema__Feed__Article__Status.TO_PROCESS:
#                 self.articles_to_process[article_id]=article
#         print(f"There are {len(self.articles_to_process)} articles to process")
#
#     @task()
#     def process_articles__create_article_file(self):
#         articles_by_location = {}                                           # todo: refactor this file load cache into a better location
#         for article_id, article in self.articles_to_process.items():
#             location               = article.path__folder__source
#             articles_by_article_id = articles_by_location.get(location)
#             if articles_by_article_id is None:                              # only load once
#                 print(f'loading data for location: {location}')
#                 path_data              = self.hacker_news_data.feed_data__in_path(path=location, load_from_live=True)
#                 articles_list          = path_data.feed_data.json().get('articles')
#                 articles_by_article_id = list_index_by(articles_list, 'article_obj_id')
#                 articles_by_location[location] = articles_by_article_id
#
#             if article_id in articles_by_article_id:
#                 article_storage             = Hacker_News__Storage__Article(article_id=article_id)
#                 s3_path                     = article_storage.path__path(path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
#                 article.path__file__feed_article  = s3_path
#                 file_exists                 = article_storage.path__exists(s3_path=s3_path)
#                 if file_exists is False:
#                     #s3_path = article_storage.path__path(path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
#                     article_data = articles_by_article_id.get(article_id)
#                     s3_path      = article_storage.save_to__path(data=article_data, path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
#                     print(f"created file {s3_path}")
#
#                     #pprint(article_storage.load_from__path(location, S3_FILE_NAME__ARTICLE__FEED_ARTICLE, S3_Key__File_Extension.JSON))
#                 article.status = Schema__Feed__Article__Status.TO_EXTRACT_TEXT
#
#         self.hacker_news_edit.save__current_articles(self.current_articles)
#
#     def extract_entities_from_text(self, text):                             # todo: move this to a separate class
#
#         from mgraph_db.providers.graph_rag.actions.Graph_RAG__Document__Processor import Graph_RAG__Document__Processor
#         from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI         import API__LLM__Open_AI
#         api_llm       = API__LLM__Open_AI()
#         processor     = Graph_RAG__Document__Processor(api_llm=api_llm)                 # GraphRAG Create processor instance
#         entities      = processor.extract_entities(text=text)
#         text_entities = Schema__Feed__Text__Entities(text=text, entities=entities)
#         return text_entities
#
#     @task()
#     def process_articles__create_text_entities(self):
#         if env_value('OPEN_AI__API_KEY') is None:
#             print("OpenAi key not available")
#             self.result__create_text_entities['error'] = "OpenAi key not available"
#             return
#
#         for article_id, article in self.current_articles.articles.items():
#             if article.status == Schema__Feed__Article__Status.TO_EXTRACT_TEXT:
#                 article_storage = Hacker_News__Storage__Article(article_id=article_id)
#                 path__feed_article    = article.path__file__feed_article
#                 article_data          = article_storage.path__load_data(path__feed_article)     # todo: we shouldn't be using a dict here (we should be using .data() and get the correct schema file
#                 article_title         = article_data.get('title'     )
#                 article_description   = article_data.get('description')
#
#                 with capture_duration() as duration__title:
#                     entities__title       = self.extract_entities_from_text  (article_title    )
#                 with capture_duration() as duration__description:
#                     entities__description = self.extract_entities_from_text(article_description)
#
#                 article_entities      = Schema__Feed__Article__Entities(entities__title=entities__title, entities__description=entities__description)
#
#                 location = article.path__folder__source
#                 data     = article_entities.json()
#                 s3_path  = article_storage.save_to__path(data      = data                                 ,
#                                                          path      = location                             ,
#                                                          file_id   = S3_FILE_NAME__ARTICLE__TEXT_ENTITIES ,
#                                                          extension = S3_Key__File_Extension.JSON          )
#
#                 result = dict(article_id             = article_id                                         ,
#                               s3_path                = s3_path                                            ,
#                               duration__title        = duration__title.seconds                            ,
#                               duration__description  = duration__description.seconds                      ,
#                               entities__title        = len(article_entities.entities__title.entities      ),
#                               entities__description  = len(article_entities.entities__description.entities))
#
#                 self.result__create_text_entities[article_id] = result
#                 article.next_step = Schema__Feed__Article__Step.STEP__3__CREATE_GRAPH
#                 if len(self.result__create_text_entities) >= DEFAULT__MAX_ARTICLES_TO_PROCESS:
#                     break
#         self.hacker_news_edit.save__current_articles(self.current_articles)
#
#
#     @flow()
#     def process_articles(self) -> Flow:
#         self.load_new_articles()
#         self.process_articles__create_article_file ()
#         self.process_articles__create_text_entities()
#         return self.result__create_text_entities
#
#
#     def run(self):
#         return self.process_articles().execute_flow()