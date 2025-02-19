from typing                                                                       import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                               import Schema__MGraph__Types
from myfeeds_ai.mgraphs.articles_index.schemas.Schema__Article__Index__Node       import Schema__Article__Index__Node
from myfeeds_ai.mgraphs.articles_index.schemas.Schema__Article__Index__Node__Data import Schema__Article__Index__Node__Data


class Schema__Article__Index__Types(Schema__MGraph__Types):             # Types used in article index graphs
    node_type      : Type[Schema__Article__Index__Node]
    node_data_type : Type[Schema__Article__Index__Node__Data]