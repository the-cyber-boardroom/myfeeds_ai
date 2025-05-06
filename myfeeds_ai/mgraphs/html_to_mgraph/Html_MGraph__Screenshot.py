from enum import Enum
from typing import Dict, Type

from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Layout__Engine import \
    MGraph__Export__Dot__Layout__Engine

from mgraph_db.mgraph.MGraph                                        import MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Config__Node    import Html_MGraph__Config__Node, HTML_MGRAPH__NODES__CONFIG
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.utils.Dev                                          import pprint



# ========================================================================================
# Global Configuration
# ========================================================================================

class Html_MGraph__Screenshot__Config__Graph(Type_Safe):
    """Graph-wide configuration settings"""
    title           : str = "HTML Document Structure"
    title_font_size : int = 30
    title_font_color: str = "#333333"
    bg_color        : str = "#f8f9fa"
    rank_sep        : float = 1.0           # vertical separation distance
    node_sep        : float = 0.8           # distance between nodes
    margin          : float = 0.2           # graph margin
    layout_engine   : MGraph__Export__Dot__Layout__Engine = None
    spring_constant : float = None          # string strength in FDP

class Html_MGraph__Screenshot__Config(Type_Safe):                    # Main configuration class for HTML MGraph screenshots
    graph         : Html_MGraph__Screenshot__Config__Graph
    target_file   : str  = None
    print_dot_code: bool = False
    node_configs  : Dict[Type, Html_MGraph__Config__Node]             # Optional overrides for specific node/edge configs

    def get_node_config(self, node_type: Type) -> Html_MGraph__Config__Node:    # Get configuration for a specific node type, with overrides if specified
        if node_type in self.node_configs:
            return self.node_configs[node_type]
        return HTML_MGRAPH__NODES__CONFIG.get(node_type, Html_MGraph__Config__Node())

# ========================================================================================
# Screenshot Creation Class
# ========================================================================================

class Html_MGraph__Screenshot(Type_Safe):
    html_mgraph: MGraph
    create_png : bool = True

    def create(self, config: Html_MGraph__Screenshot__Config):          # Create a screenshot of the HTML graph with the specified configuration
        with self.html_mgraph.screenshot() as _:
            with _.export().export_dot() as dot:

                if config.graph.layout_engine:                                          # Configure graph settings
                    dot.set_graph__layout_engine(config.graph.layout_engine.value)
                if config.graph.spring_constant:
                    dot.set_graph__spring_constant(config.graph.spring_constant)
                dot.set_graph__rank_sep(config.graph.rank_sep)
                dot.set_graph__node_sep(config.graph.node_sep)
                dot.set_graph__margin(config.graph.margin)


                if config.graph.title:                                                  # Set graph title
                    dot.set_graph__title(config.graph.title)
                    dot.set_graph__title__font__size(config.graph.title_font_size)
                    dot.set_graph__title__font__color(config.graph.title_font_color)

                dot.set_graph__background__color(config.graph.bg_color)

                # Content display settings
                dot.show_node__value()

                # Apply node styling for each node type
                for node_type, node_config in HTML_MGRAPH__NODES__CONFIG.items():
                    cfg = config.get_node_config(node_type)                                 # Get configuration, potentially with overrides

                    # Apply styling
                    if cfg.fill_color: dot.set_node__type_fill_color(node_type, cfg.fill_color)
                    if cfg.font_color: dot.set_node__type_font_color(node_type, cfg.font_color)
                    if cfg.shape     : dot.set_node__type_shape     (node_type, cfg.shape     )
                    if cfg.style     : dot.set_node__type_style     (node_type, cfg.style     )
                    if cfg.font_size : dot.set_node__type_font_size (node_type, cfg.font_size )
                    if cfg.font_name : dot.set_node__type_font_name (node_type, cfg.font_name )


            # Save the graph
            _.save_to(target_file=config.target_file).dot(print_dot_code=config.print_dot_code)