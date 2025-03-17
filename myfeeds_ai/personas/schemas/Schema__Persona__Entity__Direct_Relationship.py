from osbot_utils.type_safe.Type_Safe                     import Type_Safe


class Schema__Persona__Entity__Direct_Relationship(Type_Safe):
    entity            : str
    relationship_type : str
    strength          : float    # strength level (between 0 and 1)