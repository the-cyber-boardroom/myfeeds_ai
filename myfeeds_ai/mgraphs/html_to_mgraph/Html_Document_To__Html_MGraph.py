from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Layout__Engine import \
    MGraph__Export__Dot__Layout__Engine

from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value import Schema__MGraph__Node__Value

from mgraph_db.mgraph.schemas.Schema__MGraph__Node import Schema__MGraph__Node

from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.MGraph                                        import MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph import Html_MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Schemas import HTML__EDGES_TYPES__FOR__TAG, \
    HTML__NODES_TYPES__FOR__TAG, Schema__MGraph__NODE__HTML__TEXT, Schema__MGraph__Edge__HTML__TEXT
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Screenshot import Html_MGraph__Screenshot__Config
from osbot_utils.helpers.Obj_Id                                     import Obj_Id
from osbot_utils.helpers.html.Html__To__Html_Document               import Html__To__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Document         import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node             import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data       import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type
from osbot_utils.helpers.safe_str.Safe_Str__Html                    import Safe_Str__Html
from osbot_utils.type_safe.Type_Safe                                import Type_Safe








MAX__NODE_DATA__DISPLAY__VALUE = 10

class Html_Document_To__Html_MGraph(Type_Safe):
    html          : Safe_Str__Html         = None
    html__document: Schema__Html_Document  = None
    html_mgraph   : Html_MGraph

    def convert(self):
        with Html__To__Html_Document(html=self.html).convert() as _:
            self.html__document = _
            self.build_mgraph__from__html_node(_.root_node)
        return self.html_mgraph

    def resolve_edge_type_from_node_tag(self, node_tag):
        return HTML__EDGES_TYPES__FOR__TAG.get(node_tag, None)

    def resolve_node_type_from_node_tag(self, node_tag):
        return HTML__NODES_TYPES__FOR__TAG.get(node_tag, None)

    def resolve_node_data(self,node: Schema__Html_Node__Data):
        node_data      = node.data
        node_data_size = len(node_data)

        return f"({node_data_size})"
        if node_data_size < MAX__NODE_DATA__DISPLAY__VALUE:
            return node_data
        else:
            return f"{node_data[0:MAX__NODE_DATA__DISPLAY__VALUE]} ... ({node_data_size})"

    def build_mgraph__from__html_node(self, target_node: Schema__Html_Node):
        #print(type(parent_node))
        with self.html_mgraph.builder() as _:
            node_tag  = target_node.tag
            node_type = self.resolve_node_type_from_node_tag(node_tag)
            _.add_node(node_tag, key=Obj_Id(), node_type=node_type)
            # if parent_node:
            #     _.connect_to(parent_node.node_id)
            for node in target_node.nodes:
                if type(node) is Schema__Html_Node:
                    edge_type = self.resolve_edge_type_from_node_tag(node.tag)
                    child_node = self.build_mgraph__from__html_node(node)
                    _.connect_to(target=child_node.node_id, edge_type=edge_type)
                    #_.add_predicate(node.tag, child_node.node_id)
                    _.up()
                elif type(node) is Schema__Html_Node__Data:
                    if node.type == Schema__Html_Node__Data__Type.TEXT:
                        node_data = self.resolve_node_data(node)
                        _.add_node(node_data, key=Obj_Id(), node_type=Schema__MGraph__NODE__HTML__TEXT)
                        text_node = _.current_node()
                        _.up()
                        _.connect_to(text_node.node_id, edge_type=Schema__MGraph__Edge__HTML__TEXT)

                    #key = Obj_Id()
                    #_.add_node(node.tag, key=key)
                    #print(type(_.current_node()))


            _.up()
            return _.current_node()


    def convert__to__html_schema(self):
        with Html__To__Html_Document(html=self.html).convert() as _:
            self.html__document = _
            self.build_mgraph__with__html_schema(_.root_node)
        return self.html_mgraph

    def build_mgraph__with__html_schema(self, target_node: Schema__Html_Node):
        with self.html_mgraph.builder() as _:

            _.add_node(target_node.tag)
            for node in target_node.nodes:
                if type(node) is Schema__Html_Node:
                    self.build_mgraph__with__html_schema(node)
                    _.connect_to(node.tag, unique_link=True)
                    _.up()



    # def create_screenshot_2(self, target_file=None):
    #     with self.html_mgraph.screenshot() as _:
    #
    #         with _.export().export_dot() as dot:
    #             dot.set_node__shape__type__box()
    #             dot.set_node__shape__rounded()
    #             dot.set_graph__layout_engine__fdp()
    #             dot.show_node__value()
    #             dot.set_edge_from_node__type_shape     (Schema__MGraph__Edge__HTML__BODY, 'point')
    #             dot.set_edge_to_node__type_fill_color  (Schema__MGraph__Edge__HTML__BODY, 'grey'  )
    #             dot.set_edge_to_node__type_fill_color  (Schema__MGraph__Edge__HTML__P,    'blue' )
    #             dot.set_node__type_fill_color          (Schema__MGraph__NODE__HTML__HEAD, 'red')
    #             dot.set_node__type_fill_color          (Schema__MGraph__NODE__HTML__P   , 'green')
    #             dot.set_edge_to_node__type_font_color  (Schema__MGraph__Edge__HTML__P   , 'white')
    #             dot.set_edge_from_node__type_font_color(Schema__MGraph__Edge__HTML__P   , 'red'  )
    #
    #             dot.set_node__type_fill_color          (Schema__MGraph__NODE__HTML__TEXT, 'black')
    #             dot.set_node__type_font_color          (Schema__MGraph__NODE__HTML__TEXT, 'white')
    #
    #             dot.set_node__type_shape               (Schema__MGraph__NODE__HTML__TEXT, 'box')
    #             dot.set_node__type_shape               (Schema__MGraph__NODE__HTML__P   , 'box')
    #             dot.set_node__shape__type__point()
    #             dot.set_edge__arrow_head__none()
    #
    #         _.save_to(target_file=target_file).dot()

    def create_screenshot(self, config: Html_MGraph__Screenshot__Config):
        # config_kwargs = dict(#layout      = MGraph__Export__Dot__Layout__Engine.FDP,
        #                      target_file = target_file                          )
        #config = Html_MGraph__Screenshot__Config(**config_kwargs)
        self.html_mgraph.html_mgraph__screenshot().create(config=config)

    def create_screenshot_2(self, target_file=None):
        with self.html_mgraph.screenshot() as _:
            with _.export().export_dot() as dot:
                # Base graph configuration - use a hierarchical layout
                dot.set_graph__layout_engine__dot()  # Hierarchical layout (top-down)
                dot.set_graph__rank_dir__tb()        # Top to bottom direction
                dot.set_graph__splines__ortho()      # Right-angle edges for cleaner appearance
                dot.set_graph__rank_sep(1.8)         # More vertical space between ranks
                dot.set_graph__node_sep(0.6)         # Horizontal separation between nodes
                dot.set_graph__margin(0.3)           # Graph margin

                # Set graph title
                dot.set_graph__title("HTML Document Structure")
                dot.set_graph__title__font__size(20)
                dot.set_graph__title__font__color("#333333")
                dot.set_graph__background__color("#f9fafb")

                # Base node styling
#                dot.set_node__shape__fixed()         # Fixed-size nodes for consistency
                dot.set_node__shape__width(1.5)      # Width of nodes
                dot.set_node__shape__height(0.8)     # Height of nodes
                dot.set_node__font__size(11)
                dot.set_node__font__name("Arial")
                #
                # Edge styling
                dot.set_edge__arrow_size(0.7)
                dot.set_edge__style("solid")
                dot.set_edge__color("#8899aa")

                # Content display settings - show only essential info
                #dot.config.display.node_value = True       # Show node values
                dot.config.display.node_type = False       # Don't show node types (cleaner)
                dot.config.display.edge_ids = False        # Don't show edge IDs

                # HTML element styling with distinctive color scheme

                # HTML element - root element
                dot.set_node__type_fill_color(Schema__MGraph__NODE__HTML__HTML, "#2563eb")  # Blue
                dot.set_node__type_font_color(Schema__MGraph__NODE__HTML__HTML, "#ffffff")
                dot.set_node__type_shape(Schema__MGraph__NODE__HTML__HTML, "doubleoctagon")
                dot.set_node__type_style(Schema__MGraph__NODE__HTML__HTML, "filled")

                # HEAD element - structural element
                dot.set_node__type_fill_color(Schema__MGraph__NODE__HTML__HEAD, "#dc2626")  # Red
                dot.set_node__type_font_color(Schema__MGraph__NODE__HTML__HEAD, "#ffffff")
                dot.set_node__type_shape(Schema__MGraph__NODE__HTML__HEAD, "hexagon")
                dot.set_node__type_style(Schema__MGraph__NODE__HTML__HEAD, "filled")

                # BODY element - main content container
                dot.set_node__type_fill_color(Schema__MGraph__NODE__HTML__BODY, "#16a34a")  # Green
                dot.set_node__type_font_color(Schema__MGraph__NODE__HTML__BODY, "#ffffff")
                dot.set_node__type_shape(Schema__MGraph__NODE__HTML__BODY, "box")
                dot.set_node__type_style(Schema__MGraph__NODE__HTML__BODY, "rounded,filled")

                # P elements - paragraphs
                dot.set_node__type_fill_color(Schema__MGraph__NODE__HTML__P, "#9333ea")  # Purple
                dot.set_node__type_font_color(Schema__MGraph__NODE__HTML__P, "#ffffff")
                dot.set_node__type_shape(Schema__MGraph__NODE__HTML__P, "note")
                dot.set_node__type_style(Schema__MGraph__NODE__HTML__P, "filled")

                # TEXT elements - actual text content
                dot.set_node__type_fill_color(Schema__MGraph__NODE__HTML__TEXT, "#1e293b")  # Dark slate
                dot.set_node__type_font_color(Schema__MGraph__NODE__HTML__TEXT, "#ffffff")
                dot.set_node__type_shape(Schema__MGraph__NODE__HTML__TEXT, "box")
                dot.set_node__type_style(Schema__MGraph__NODE__HTML__TEXT, "rounded,filled")

                # Edge styling based on the parent element type

                # HTML element connections
                dot.set_edge__type_color(Schema__MGraph__Edge__HTML__HTML, "#2563eb")
                dot.set_edge__type_style(Schema__MGraph__Edge__HTML__HTML, "bold")

                # HEAD connections
                dot.set_edge__type_color(Schema__MGraph__Edge__HTML__HEAD, "#dc2626")

                # BODY connections
                dot.set_edge__type_color(Schema__MGraph__Edge__HTML__BODY, "#16a34a")

                # P connections
                dot.set_edge__type_color(Schema__MGraph__Edge__HTML__P, "#9333ea")

                # TEXT connections - use dotted lines for text nodes
                dot.set_edge__type_color(Schema__MGraph__Edge__HTML__TEXT, "#64748b")
                dot.set_edge__type_style(Schema__MGraph__Edge__HTML__TEXT, "dotted")

                # Special handling for direct parent-child relationships to enhance readability
                # These settings help visually group related nodes

                # Make nodes connected to BODY appear related
                dot.set_edge_from_node__type_shape(Schema__MGraph__Edge__HTML__BODY, "box")
                dot.set_edge_from_node__type_style(Schema__MGraph__Edge__HTML__BODY, "rounded")

                # Special styling for paragraph connections
                dot.set_edge_to_node__type_fill_color(Schema__MGraph__Edge__HTML__P, "#9333ea")

            # Save the graph
            _.save_to(target_file=target_file).dot()
            print()
            #print(_.export().to__dot())