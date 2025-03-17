from myfeeds_ai.personas.schemas.Schema__Persona__Entities import Schema__Persona__Entities
from osbot_utils.helpers.Obj_Id                            import Obj_Id
from osbot_utils.helpers.Timestamp_Now                     import Timestamp_Now
from osbot_utils.type_safe.Type_Safe                       import Type_Safe

class Schema__Persona__Text__Entities(Type_Safe):
    cache_id     : Obj_Id                    = None
    duration     : float                     = None
    text         : str                       = None
    text_entities: Schema__Persona__Entities = None
    text_id      : Obj_Id
    timestamp    : Timestamp_Now
