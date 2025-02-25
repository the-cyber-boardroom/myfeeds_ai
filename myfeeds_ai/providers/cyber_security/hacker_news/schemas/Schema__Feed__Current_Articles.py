from enum import Enum
from typing                             import Dict
from osbot_utils.helpers.Obj_Id         import Obj_Id
from osbot_utils.type_safe.Type_Safe    import Type_Safe


class Schema__Feed__Current_Article__Status(Enum):
    TO_PROCESS         : str = 'to-process'
    PROCESSED          : str = 'processed'
    ERROR__NO_FEED_DATA: str = 'error-no-feed-data'
    ERROR__IN_PROCESS  : str = 'error-in-process'


class Schema__Feed__Current_Article(Type_Safe):
    knowledge_graph   : bool
    llm_prompt        : bool
    location          : str
    status            : Schema__Feed__Current_Article__Status = Schema__Feed__Current_Article__Status.TO_PROCESS
    path__feed_article: str = None


class Schema__Feed__Current_Articles(Type_Safe):
    articles: Dict[Obj_Id, Schema__Feed__Current_Article]
