from typing import Dict

from myfeeds_ai.personas.llms.Schema__Persona__Connected_Entities import Schema__Persona__Connected_Entities
from osbot_utils.helpers.Obj_Id                                   import Obj_Id
from osbot_utils.type_safe.Type_Safe                              import Type_Safe


class Schema__Persona__LLM__Connect_Entities(Type_Safe):
    cache_id__llm_request                : Obj_Id                              = None
    persona__path_now                    : str                                 = None
    path_now__text_entities__titles__tree: str                                 = None
    connected_entities                   : Schema__Persona__Connected_Entities = None
    articles_markdown                    : Dict[Obj_Id,str]
