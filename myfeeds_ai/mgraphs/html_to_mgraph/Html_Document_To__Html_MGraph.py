from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph                  import Html_MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Schemas         import HTML__EDGES_TYPES__FOR__TAG, HTML__NODES_TYPES__FOR__TAG, Schema__MGraph__NODE__HTML__TEXT, Schema__MGraph__Edge__HTML__TEXT
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Screenshot      import Html_MGraph__Screenshot__Config
from osbot_utils.helpers.Obj_Id                                     import Obj_Id
from osbot_utils.helpers.html.Html__To__Html_Document               import Html__To__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Document         import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node             import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data       import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type
from osbot_utils.helpers.safe_str.Safe_Str__Html                    import Safe_Str__Html
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

#MAX__NODE_DATA__DISPLAY__VALUE = 10

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
        # if node_data_size < MAX__NODE_DATA__DISPLAY__VALUE:
        #     return node_data
        # else:
        #     return f"{node_data[0:MAX__NODE_DATA__DISPLAY__VALUE]} ... ({node_data_size})"

    def build_mgraph__from__html_node(self, target_node: Schema__Html_Node):
        with self.html_mgraph.builder() as _:
            node_tag  = target_node.tag
            node_type = self.resolve_node_type_from_node_tag(node_tag)
            _.add_node(node_tag, key=Obj_Id(), node_type=node_type)
            for node in target_node.nodes:
                if type(node) is Schema__Html_Node:
                    edge_type = self.resolve_edge_type_from_node_tag(node.tag)
                    child_node = self.build_mgraph__from__html_node(node)
                    _.connect_to(target=child_node.node_id, edge_type=edge_type)
                    _.up()
                elif type(node) is Schema__Html_Node__Data:
                    if node.type == Schema__Html_Node__Data__Type.TEXT:
                        node_data = self.resolve_node_data(node)
                        _.add_node(node_data, key=Obj_Id(), node_type=Schema__MGraph__NODE__HTML__TEXT)
                        text_node = _.current_node()
                        _.up()
                        _.connect_to(text_node.node_id, edge_type=Schema__MGraph__Edge__HTML__TEXT)

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

    def create_screenshot(self, config: Html_MGraph__Screenshot__Config):
        self.html_mgraph.html_mgraph__screenshot().create(config=config)