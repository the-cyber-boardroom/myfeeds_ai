from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Current_Articles import \
    Hacker_News__File__Current_Articles
from osbot_utils.helpers.flows.Flow import Flow
from osbot_utils.helpers.flows.decorators.flow import flow
from osbot_utils.helpers.flows.decorators.task import task
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint


class Flow__Hacker_News__4__Create_Article_Files(Type_Safe):
    file_current_articles : Hacker_News__File__Current_Articles
    output : dict

    @task()
    def task__1__load_new_articles(self):
        articles_to_process = self.file_current_articles.to__process()
        #pprint(articles_to_process)
        # self.current_articles = self.hacker_news_data.current_articles()
        # for article_id, article in self.current_articles.articles.items():
        #     if article.status == Schema__Feed__Current_Article__Status.TO_PROCESS:
        #         self.articles_to_process[article_id]=article
        #print(f"There are {len(self.articles_to_process)} articles to process")

    def task__5__create_output(self):
        self.output = dict()

    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__5__create_output()
        return self.output


    def run(self):
        return self.process_articles().execute_flow()