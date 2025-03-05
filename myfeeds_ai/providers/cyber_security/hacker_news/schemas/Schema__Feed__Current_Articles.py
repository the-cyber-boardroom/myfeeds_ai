from typing                                                                                         import Dict
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Article__Status  import Schema__Feed__Current_Article__Status, Schema__Feed__Current_Article__Step
from osbot_utils.helpers.Obj_Id                                                                     import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe

class Schema__Feed__Current_Article(Type_Safe):
    article_id                 : Obj_Id
    source_location            : str
    next_step                  : Schema__Feed__Current_Article__Step = Schema__Feed__Current_Article__Step.STEP__1__SAVE_ARTICLE
    status                     : Schema__Feed__Current_Article__Status    = Schema__Feed__Current_Article__Status.TO_PROCESS
    path__feed_article         : str = None
    path__entities_mgraph__json: str = None
    path__entities_mgraph__png : str = None

class Schema__Feed__Current_Article__Status__Change(Type_Safe):
    article     : Schema__Feed__Current_Article
    from_status : Schema__Feed__Current_Article__Status
    from_step   : Schema__Feed__Current_Article__Step

class Schema__Feed__Current_Articles(Type_Safe):
    articles: Dict[Obj_Id, Schema__Feed__Current_Article]
