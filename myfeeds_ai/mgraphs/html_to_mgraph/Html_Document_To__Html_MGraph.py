from mgraph_db.mgraph.MGraph import MGraph

from osbot_utils.helpers.html.Html__To__Html_Document       import Html__To__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Document import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node import Schema__Html_Node
from osbot_utils.helpers.safe_str.Safe_Str__Html            import Safe_Str__Html
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Html_Document_To__Html_MGraph(Type_Safe):
    html          : Safe_Str__Html         = None
    html__document: Schema__Html_Document  = None
    html_mgraph   : MGraph

    def convert(self):
        with Html__To__Html_Document(html=self.html).convert() as _:
                self.html__document = _
                self.build_mgraph__from__html_node(_.root_node)
        return self.html_mgraph

    def build_mgraph__from__html_node(self, target_node: Schema__Html_Node):
        with self.html_mgraph.builder() as _:

            _.add_node(target_node.tag)
            for node in target_node.nodes:
                if type(node) is Schema__Html_Node:
                    self.build_mgraph__from__html_node(node)
                    _.connect_to(node.tag, unique_link=True)
                    _.up()




#     def build_mgraph__from__html_node(self, target_node: Schema__Html_Node, parent_node: Domain__MGraph__Node = None):
#         print(type(parent_node))
#         with self.html_mgraph.builder() as _:
#             _.add_node(target_node.tag)
#             for node in target_node.nodes:
#                 if type(node) is Schema__Html_Node:
#                     self.build_mgraph__from__html_node(node)
#                     key = Obj_Id()
#                     _.add_node(node.tag, key=key)
#                     print(type(_.current_node()))
#
#                     #_.up()