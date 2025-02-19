from mgraph_ai.mgraph.schemas.Schema__MGraph__Node                          import Schema__MGraph__Node
from myfeeds_ai.mgraphs.articles_index.schemas.Schema__Article__Index__Node__Data import Schema__Article__Index__Node__Data

class Schema__Article__Index__Node(Schema__MGraph__Node):                   # Schema for article index nodes
    node_data : Schema__Article__Index__Node__Data