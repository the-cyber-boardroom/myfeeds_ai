from typing                                              import List
from myfeeds_ai.personas.schemas.Schema__Persona__Entity import Schema__Persona__Entity
from osbot_utils.type_safe.Type_Safe                     import Type_Safe

class Schema__Persona__Entities(Type_Safe):
    entities: List[Schema__Persona__Entity]