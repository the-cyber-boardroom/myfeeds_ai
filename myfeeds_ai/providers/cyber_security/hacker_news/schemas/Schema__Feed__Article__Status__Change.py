from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article          import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status  import Schema__Feed__Article__Status
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step    import Schema__Feed__Article__Step
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe

class Schema__Feed__Article__Status__Change(Type_Safe):
    article     : Schema__Feed__Article
    from_status : Schema__Feed__Article__Status
    from_step   : Schema__Feed__Article__Step