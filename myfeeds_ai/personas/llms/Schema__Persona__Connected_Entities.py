from typing                                            import List, Dict, Any
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Schema__Persona__Entity_Match(Type_Safe):
    """Represents a specific entity match between persona interest and article."""
    persona_entity : str                         # Name of the matching entity from the Persona Tree Graph
    article_entity : str                         # Name of the matching entity from the Article Tree Graph
    relevance_score: float                       # Score from 0.0 to 1.0 indicating match strength
    persona_context: str                         # How this relates to the persona's interests (from the Persona Graph Tree)
    article_context: str                         # How this appears in the article  (from the Article Graph Tree)
    match_type     : str                         # Type of match (direct, semantic, contextual)

# class Schema__Persona__Relationship_Match(Type_Safe):
#     """Represents a relationship match between persona interests and article."""
#     persona_entity      : str                     # Source entity in the relationship (from the Persona Graph Tree)
#     article_entity      : str                     # Target entity in the relationship (from the Article Graph Tree)
#     relationship_type  : str                     # Type of relationship
#     relevance_score    : float                   # Score from 0.0 to 1.0 indicating match strength
#     persona_context    : str                     # How this relationship exists in persona interests
#     article_context    : str                     # How this relationship is represented in article

class Schema__Persona__Connected_Entity(Type_Safe):
    """Complete relevance assessment between a persona and an article."""
    article_id          : str                     # The ID of the article
    overall_score       : float                   # Overall relevance score (0.0-10.0)
    entity_matches      : List[Schema__Persona__Entity_Match      ]
    #relationship_matches: List[Schema__Persona__Relationship_Match]
    primary_relevance   : List[str]               # Primary areas of relevance to persona responsibilities
    relevance_summary   : str                     # Summary explanation of relevance
    priority_level      : str                     # Urgency level (critical, high, medium, low)
    #key_insights        : List[str]               # Key takeaways for the persona

class Schema__Persona__Connected_Entities(Type_Safe):
    connected_entities : List[Schema__Persona__Connected_Entity]    # multiple articles mappings for this persona