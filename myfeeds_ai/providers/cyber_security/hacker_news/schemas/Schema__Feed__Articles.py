from typing                                                                        import Dict
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article import Schema__Feed__Article
from osbot_utils.helpers.Obj_Id                                                    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe

class Schema__Feed__Articles(Type_Safe):
    articles: Dict[Obj_Id, Schema__Feed__Article]
