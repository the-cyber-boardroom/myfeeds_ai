from typing                                                                                     import Dict, List
from myfeeds_ai.personas.llms.Schema__Persona__Connected_Entities                               import Schema__Persona__Connected_Entity
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Text_Entities__Files import Schema__Feed__Text_Entities__Files
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                                          import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe


class Schema__Persona__Articles__Connected_Entities(Type_Safe):
    cache_id__llm_request                    : Obj_Id                                  = None
    path__now                                : Safe_Str__File__Path                    = None
    path__now__persona                       : Safe_Str__File__Path                    = None
    path__now__persona__tree_values          : Safe_Str__File__Path                    = None
    paths__feed__text_entities               : Schema__Feed__Text_Entities__Files
    connected_entities                       : List[Schema__Persona__Connected_Entity] = None
    articles_markdown                        : Dict[Obj_Id,str]
