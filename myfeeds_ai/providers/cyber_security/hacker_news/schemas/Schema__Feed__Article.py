from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status import Schema__Feed__Article__Status
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step   import Schema__Feed__Article__Step
from osbot_utils.helpers.Obj_Id                                                            import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                       import Type_Safe


class Schema__Feed__Article(Type_Safe):
    article_id                 : Obj_Id
    source_location            : str
    next_step                  : Schema__Feed__Article__Step   = Schema__Feed__Article__Step.STEP__1__SAVE_ARTICLE
    status                     : Schema__Feed__Article__Status = Schema__Feed__Article__Status.TO_PROCESS
    path__feed_article         : str = None
    path__entities_mgraph__json: str = None
    path__entities_mgraph__png : str = None
