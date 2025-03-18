from typing import List, Annotated, Literal
from myfeeds_ai.personas.schemas.Schema__Persona__Entity__Direct_Relationship import Schema__Persona__Entity__Direct_Relationship
from osbot_utils.type_safe.Type_Safe                                          import Type_Safe

class Schema__Persona__Entity(Type_Safe):
    direct_relationships : List[Schema__Persona__Entity__Direct_Relationship]      # Relationships with other entities found in the text
    name                 : str                                                       # Core entity name