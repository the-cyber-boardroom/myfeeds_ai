from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph                                      import Html_MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Screenshot__Config  import Schema__Html_MGraph__Screenshot__Config
from osbot_utils.helpers.html.schemas.Schema__Html_Document                             import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node                                 import Schema__Html_Node
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe

class Html_Document__To__Html_MGraph__Schema(Type_Safe):
    html_document: Schema__Html_Document = None
    html_mgraph  : Html_MGraph

    def convert(self):
        target_node = self.html_document.root_node
        self.build_mgraph__with__html_schema(target_node=target_node)
        return self.html_mgraph

    def build_mgraph__with__html_schema(self, target_node: Schema__Html_Node):
        with self.html_mgraph.builder() as _:
            _.add_node(target_node.tag)
            for node in target_node.nodes:
                if type(node) is Schema__Html_Node:
                    self.build_mgraph__with__html_schema(node)
                    _.connect_to(node.tag, unique_link=True)
                    _.up()

    def screenshot(self, target_file = None):
        with Schema__Html_MGraph__Screenshot__Config() as _:
            _.target_file = target_file
            png_bytes     = self.html_mgraph.html_mgraph__screenshot().create(config=_)
            return png_bytes

    def tree_values(self):
        html_node = self.html_mgraph.node__html()
        if html_node:
            with self.html_mgraph.export().export_tree_values(show_predicate=False) as _:
                return _.as_text(root_nodes_ids=[html_node.node_id])

