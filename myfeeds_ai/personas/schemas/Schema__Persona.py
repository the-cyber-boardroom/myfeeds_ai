from myfeeds_ai.personas.schemas.Schema__Persona__Entities import Schema__Persona__Entities
from osbot_utils.type_safe.Type_Safe                       import Type_Safe


class Schema__Persona(Type_Safe):
    description           : str
    description__entities : Schema__Persona__Entities
    path_now              : str
    path_latest           : str