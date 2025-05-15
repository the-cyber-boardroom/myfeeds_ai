from mgraph_db.mgraph.MGraph                                                            import MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Config__Node        import HTML_MGRAPH__NODES__CONFIG
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Screenshot__Config  import Schema__Html_MGraph__Screenshot__Config
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe

class Html_MGraph__Screenshot(Type_Safe):
    html_mgraph: MGraph
    png_bytes  : bytes = None

    def create(self, config: Schema__Html_MGraph__Screenshot__Config=None):          # Create a screenshot of the HTML graph with the specified configuration
        if not config:
            config = Schema__Html_MGraph__Screenshot__Config()
        with self.html_mgraph.screenshot() as _:
            with _.export().export_dot() as dot:

                if config.graph.layout_engine:                                          # Configure graph settings
                    dot.set_graph__layout_engine(config.graph.layout_engine.value)
                if config.graph.spring_constant:
                    dot.set_graph__spring_constant(config.graph.spring_constant)
                dot.set_graph__rank_sep(config.graph.rank_sep)
                dot.set_graph__node_sep(config.graph.node_sep)
                dot.set_graph__margin(config.graph.margin)

                #dot.show_node__id()
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
            _.save_to(target_file=config.target_file)
            self.png_bytes = _.dot(print_dot_code=config.print_dot_code)
            return self.png_bytes