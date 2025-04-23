from typing                          import List
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__RDF__Triple(Type_Safe):
    subject: str
    predicate: str
    object   : str


class Schema__RDF__Triples(Type_Safe):
    triplets: List[Schema__RDF__Triple]

