from typing import List

from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Current_Articles import \
    Hacker_News__File__Current_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles import \
    Schema__Feed__Current_Article
from osbot_utils.helpers.flows.Flow import Flow
from osbot_utils.helpers.flows.decorators.flow import flow
from osbot_utils.helpers.flows.decorators.task import task
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint


class Flow__Hacker_News__4__Create_Article_Files(Type_Safe):
    file_current_articles : Hacker_News__File__Current_Articles
    output                : dict
    articles_to_process   : List[Schema__Feed__Current_Article]

    @task()
    def task__1__load_new_articles(self):
        with self.file_current_articles as _:
            _.load()
            self.articles_to_process = _.to__process()
            #print(f"There are {len(self.articles_to_process)} articles to process")

    def task__5__create_output(self):
        self.output = dict(articles_to_process=len(self.articles_to_process))

    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__5__create_output()
        return self.output


    def run(self):
        return self.process_articles().execute_flow()