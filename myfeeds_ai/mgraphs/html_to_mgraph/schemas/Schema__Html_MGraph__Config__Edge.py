# todo: see if we need this

# ========================================================================================
# Edge Configuration Classes
# ========================================================================================

# class Schema__tml_MGraph__Config__Edge(Type_Safe):
#     """Base configuration class for all HTML edges"""
#     color       : str = "#555555"  # Default gray color
#     style       : str = "solid"    # Default solid line style
#     arrow_head  : str = "vee"      # Default arrow style
#     arrow_size  : float = 0.6      # Default arrow size
#
# class Html_MGraph__Config__Edge__HTML(Html_MGraph__Config__Edge):
#     """Configuration for HTML root element edges"""
#     color       : str = "#3498db"  # Blue
#     style       : str = "bold"     # Bold lines
#
# class Html_MGraph__Config__Edge__HEAD(Html_MGraph__Config__Edge):
#     """Configuration for HEAD element edges"""
#     color       : str = "#e74c3c"  # Red
#
# class Html_MGraph__Config__Edge__BODY(Html_MGraph__Config__Edge):
#     """Configuration for BODY element edges"""
#     color       : str = "#2ecc71"  # Green
#
# class Html_MGraph__Config__Edge__P(Html_MGraph__Config__Edge):
#     """Configuration for P (paragraph) element edges"""
#     color       : str = "#9b59b6"  # Purple
#
# class Html_MGraph__Config__Edge__TEXT(Html_MGraph__Config__Edge):
#     """Configuration for TEXT element edges"""
#     color       : str = "#34495e"  # Dark gray/slate
#     style       : str = "dashed"   # Dashed lines

# ========================================================================================
# Mapping Schema Types to Configurations
# ========================================================================================



# EDGE_CONFIGS: Dict[Type, Html_MGraph__Config__Edge] = {
#     Schema__MGraph__Edge__HTML__HTML: Html_MGraph__Config__Edge__HTML(),
#     Schema__MGraph__Edge__HTML__HEAD: Html_MGraph__Config__Edge__HEAD(),
#     Schema__MGraph__Edge__HTML__BODY: Html_MGraph__Config__Edge__BODY(),
#     Schema__MGraph__Edge__HTML__P   : Html_MGraph__Config__Edge__P(),
#     Schema__MGraph__Edge__HTML__TEXT: Html_MGraph__Config__Edge__TEXT()
# }

# edge_configs: Dict[Type, Html_MGraph__Config__Edge]

# def get_edge_config(self, edge_type: Type) -> Html_MGraph__Config__Edge:
#     """Get configuration for a specific edge type, with overrides if specified"""
#     if self.edge_configs and edge_type in self.edge_configs:
#         return self.edge_configs[edge_type]
#     return EDGE_CONFIGS.get(edge_type, Html_MGraph__Config__Edge())


#                 for edge_type, edge_config in EDGE_CONFIGS.items():                     # Apply edge styling for each edge type
#                     cfg = config.get_edge_config(edge_type)                             # Get configuration, potentially with overrides
#                     dot.set_edge__type_color(edge_type, cfg.color)                      # Apply styling
#                     if cfg.style:
#                         dot.set_edge__type_style(edge_type, cfg.style)