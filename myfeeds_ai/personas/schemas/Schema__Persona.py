from myfeeds_ai.personas.schemas.Schema__Persona__Entities  import Schema__Persona__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types import Schema__Persona__Types
from osbot_utils.helpers.Obj_Id                             import Obj_Id
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: replace str types below with Safe_Str__* types

class Schema__Persona(Type_Safe):
    description              : str                         = None
    description__entities    : Schema__Persona__Entities   = None
    description__tree_values : str                         = None
    path_now                 : str
    path_latest              : str
    persona_type             : Schema__Persona__Types
    cache_ids                : dict[Safe_Id, Obj_Id]