from typing import List

from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import \
    Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change import \
    Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step import \
    Schema__Feed__Article__Step
from osbot_utils.helpers.flows.decorators.task import task
from osbot_utils.type_safe.Type_Safe import Type_Safe

FLOW__HACKER_NEWS__9__MAX__GRAPHS_TO_MERGE = 1

class Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs(Type_Safe):
    file_articles_current : Hacker_News__File__Articles__Current
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]
    max_graphs_to_merge   : int = FLOW__HACKER_NEWS__9__MAX__GRAPHS_TO_MERGE
    from_step             : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__6__MERGE__DAY_ENTITIES_GRAPHS
    to_step               : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__7__MERGE__FEED_ENTITIES_GRAPHS

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__6__merge_day_entities_graphs()