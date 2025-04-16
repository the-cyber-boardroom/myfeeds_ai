from myfeeds_ai.personas.schemas.Schema__Persona__Types         import Schema__Persona__Types
from myfeeds_ai.utils.shared_schemas.Str__Description           import Str__Description
from osbot_utils.helpers.safe_str.Safe_Str__File__Path          import Safe_Str__File__Path
from osbot_utils.helpers.safe_str.Safe_Str__Hash                import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe                            import Type_Safe

class Schema__Persona(Type_Safe):
    description                                : Str__Description       = None            # this is a version of Safe_Str__Text with support for ' and /
    description__hash                          : Safe_Str__Hash         = None
    path__now                                  : Safe_Str__File__Path   = None
    path__now__before                          : Safe_Str__File__Path   = None
    path__persona__articles__connected_entities: Safe_Str__File__Path   = None
    path__persona__digest                      : Safe_Str__File__Path   = None
    path__persona__digest__html                : Safe_Str__File__Path   = None
    path__persona__entities                    : Safe_Str__File__Path   = None
    path__persona__entities__png               : Safe_Str__File__Path   = None
    path__persona__entities__tree_values       : Safe_Str__File__Path   = None
    path__persona__latest                      : Safe_Str__File__Path   = None
    persona_type                               : Schema__Persona__Types