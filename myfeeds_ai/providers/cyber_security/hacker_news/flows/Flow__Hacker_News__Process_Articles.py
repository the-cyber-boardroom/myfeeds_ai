from typing import List, Dict

from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB import S3_FILE_NAME__ARTICLE__FEED_ARTICLE
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data              import Hacker_News__Data
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Live_Data import Hacker_News__Live_Data
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage           import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article import \
    Hacker_News__Storage__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles import \
    Schema__Feed__Current_Articles, Schema__Feed__Current_Article, Schema__Feed__Current_Article__Status
from osbot_utils.helpers.Obj_Id                                                             import Obj_Id
from osbot_utils.helpers.Safe_Id import Safe_Id
from osbot_utils.helpers.flows.Flow                                                         import Flow
from osbot_utils.helpers.flows.decorators.flow                                              import flow
from osbot_utils.helpers.flows.decorators.task                                              import task
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Dev                                                                  import pprint
from osbot_utils.utils.Lists import list_index_by


class Flow__Hacker_News__Process_Articles(Type_Safe):
    hacker_news_data      : Hacker_News__Data
    hacker_news_storage   : Hacker_News__Storage

    current_articles   : Schema__Feed__Current_Articles
    articles_to_process: Dict[Obj_Id,Schema__Feed__Current_Article]

    @task()
    def load_new_articles(self):
        self.current_articles = self.hacker_news_data.current_articles()
        for article_id, article_data in self.current_articles.articles.items():
            if article_data.status == Schema__Feed__Current_Article__Status.TO_PROCESS:
                self.articles_to_process[article_id]=article_data
        print(f"There are {len(self.articles_to_process)} articles to process")

    @task()
    def process_articles__create_article_file(self):
        #pprint(self.current_articles.json())

        articles_by_location = {}
        for article_id, article_data in self.articles_to_process.items():
            location               = article_data.location
            articles_by_article_id = articles_by_location.get(location)
            if articles_by_article_id is None:
                print(f'loading data for location: {location}')
                path_data              = self.hacker_news_data.feed_data__in_path(path=location, load_from_live=True)
                articles_list          = path_data.feed_data.json().get('articles')
                articles_by_article_id = list_index_by(articles_list, 'article_obj_id')
                articles_by_location[location] = articles_by_article_id
                #print(f'loaded {len(articles_by_article_id)} articles')
            #pprint(articles_by_article_id)
            # pprint(self.hacker_news_storage.load_from__path(location))
            # pprint(self.hacker_news_storage.files_in__path(location))
            #pprint(article_id)
            #pprint(article_data.json())
            if article_id in articles_by_article_id:
                article_storage = Hacker_News__Storage__Article(article_id=article_id)
                print(f'found: {article_id}')

                pprint(article_storage.load_from__path(location, S3_FILE_NAME__ARTICLE__FEED_ARTICLE, S3_Key__File_Extension.JSON))
                return
                article_data = articles_by_article_id.get(article_id)


                self.hacker_news_storage
                with self.hacker_news_storage.s3_db as _:
                    s3_path__article    = _.s3_key___article__feed_article__now(article_id)
                    s3_raw_path_article = _.s3_key__for_provider_path(s3_path__article)
                    print(s3_path__article)
                    print(s3_raw_path_article)
            break

            #break

    @flow()
    def process_articles(self) -> Flow:
        self.load_new_articles()
        self.process_articles__create_article_file()

    def run(self):
        return self.process_articles().execute_flow()