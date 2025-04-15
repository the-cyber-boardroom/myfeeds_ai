from myfeeds_ai.personas.llms.Schema__Persona__Digest_Articles  import Schema__Persona__Digest_Articles
from osbot_utils.helpers.Obj_Id                                 import Obj_Id
from osbot_utils.helpers.Timestamp_Now                          import Timestamp_Now
from osbot_utils.helpers.safe_str.Safe_Str__File__Path          import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                            import Type_Safe

class Schema__Persona__Digest(Type_Safe):
    cache_id             : Obj_Id
    digest_articles      : Schema__Persona__Digest_Articles
    #digest_html     : str
    #digest_markdown : str
    path__now            : Safe_Str__File__Path
    path__digest_html    : Safe_Str__File__Path
    path__persona        : Safe_Str__File__Path
    #path__digest_markdown: Safe_Str__File__Path
    timestamp            : Timestamp_Now