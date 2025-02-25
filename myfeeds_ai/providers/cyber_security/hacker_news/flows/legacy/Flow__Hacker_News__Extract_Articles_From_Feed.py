# from typing                                                                                 import List
# from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                     import Hacker_News__Files
# from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article     import Model__Hacker_News__Article
# from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed  import Model__Hacker_News__Data__Feed
# from osbot_utils.helpers.flows.decorators.flow                                              import flow
# from osbot_utils.helpers.flows.decorators.task                                              import task
# from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
# from osbot_utils.utils.Dev import pprint
#
#
# class Flow__Hacker_News__Extract_Articles_From_Feed(Type_Safe):
#     files    : Hacker_News__Files
#     data_feed: Model__Hacker_News__Data__Feed
#     articles : List[Model__Hacker_News__Article]
#
#     @task()
#     def task__load_current_feed(self):
#         self.data_feed = self.files.feed_data__current()
#         self.articles  = self.data_feed.feed_data.articles
#         print(f"loaded {len(self.articles)} articles")
#
#
#     @task()
#     def task__extract_articles_from_feed(self):
#         for article in self.articles[0:10]:
#             article_obj_id = article.article_obj_id
#             with self.files.s3_db as _:
#                 s3_path__article    = _.s3_key___article__feed_article__now(article_obj_id)
#                 s3_raw_path_article = _.s3_key__for_provider_path(s3_path__article)
#                 if _.s3_file_exists(s3_raw_path_article):
#                     print(f'+++ article exists in db: {article_obj_id}')
#                 else:
#                     print(f"--- article doesn't exist in db: {article_obj_id}")
#                     article_contents = article.json()
#                     _.s3_save_data(article_contents, s3_raw_path_article)
#                 print(s3_raw_path_article)
#
#             #pprint(article.json())
#
#     @flow()
#     def flow__extract_articles_from_feed(self):
#         with self as _:
#             _.task__load_current_feed                 ()
#             _.task__extract_articles_from_feed        ()
#
#
#     def run(self):
#         with self.flow__extract_articles_from_feed() as _:
#             _.execute_flow()