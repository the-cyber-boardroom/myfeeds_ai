from typing import List

from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import \
    Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles import Schema__Feed__Articles
from osbot_utils.helpers.flows.decorators.task import task
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint


class Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_Graphs(Type_Safe):
    file_articles_current : Hacker_News__File__Articles__Current
    articles_to_process   : Schema__Feed__Articles

    #@task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.articles
