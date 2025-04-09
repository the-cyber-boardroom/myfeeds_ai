from myfeeds_ai.personas.llms.Schema__Persona__Digest_Articles  import Schema__Persona__Digest_Articles
from osbot_utils.helpers.Obj_Id                                 import Obj_Id
from osbot_utils.helpers.Timestamp_Now                          import Timestamp_Now
from osbot_utils.type_safe.Type_Safe                            import Type_Safe


class Schema__Persona__Digest(Type_Safe):
    cache_id        : Obj_Id
    digest_articles : Schema__Persona__Digest_Articles
    digest_html     : str
    digest_markdown : str
    path_now        : str
    timestamp       : Timestamp_Now