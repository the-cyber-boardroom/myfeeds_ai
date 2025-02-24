from typing                             import Dict
from osbot_utils.helpers.Obj_Id         import Obj_Id
from osbot_utils.type_safe.Type_Safe    import Type_Safe


class Schema__Feed__Current_Article(Type_Safe):
    knowledge_graph : bool
    llm_prompt      : bool
    location        : str
    processed       : bool


class Schema__Feed__Current_Articles(Type_Safe):
    articles: Dict[Obj_Id, Schema__Feed__Current_Article]
