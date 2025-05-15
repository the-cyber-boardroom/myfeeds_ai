from typing                                                                                   import Dict, Type
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Config__Node              import Schema__Html_MGraph__Config__Node, HTML_MGRAPH__NODES__CONFIG
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Screenshot__Config__Graph import Schema__Html_MGraph__Screenshot__Config__Graph
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe


class Schema__Html_MGraph__Screenshot__Config(Type_Safe):                    # Main configuration class for HTML MGraph screenshots
    graph         : Schema__Html_MGraph__Screenshot__Config__Graph
    target_file   : str  = None
    print_dot_code: bool = False
    node_configs  : Dict[Type, Schema__Html_MGraph__Config__Node]             # Optional overrides for specific node/edge configs

    def get_node_config(self, node_type: Type) -> Schema__Html_MGraph__Config__Node:    # Get configuration for a specific node type, with overrides if specified
        if node_type in self.node_configs:
            return self.node_configs[node_type]
        return HTML_MGRAPH__NODES__CONFIG.get(node_type, Schema__Html_MGraph__Config__Node())
