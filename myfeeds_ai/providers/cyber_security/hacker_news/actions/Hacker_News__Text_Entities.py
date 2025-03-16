from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value                                       import Schema__MGraph__Node__Value
from mgraph_db.mgraph.MGraph                                                                    import MGraph
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Nodes                             import Schema__MGraph__RAG__Node__Entity
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article__Entities     import Hacker_News__Article__Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import Hacker_News__File__Articles__Current
from osbot_utils.decorators.methods.cache_on_self                                               import cache_on_self
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import obj


class Node_Type__Article_Id(Schema__MGraph__Node__Value): pass
class Node_Type__Entity   (Schema__MGraph__Node__Value): pass

class Hacker_News__Text_Entities(Type_Safe):
    file_articles_current : Hacker_News__File__Articles__Current
    mgraph_entities       : MGraph

    def article_entities(self, article_id: Obj_Id) -> Hacker_News__Article__Entities:
        article = self.file_articles_current.article(article_id)
        if article:
            path_folder_data = article.path__folder__data
            article_entities = Hacker_News__Article__Entities(article_id=article_id, path__folder__data=path_folder_data)
            return article_entities

    def add_text_entities_mgraph(self, article_id: Obj_Id, mgraph_text_entities: MGraph) -> MGraph:

        data = mgraph_text_entities.data()

        entities = []
        with mgraph_text_entities.index() as _:
            entities_nodes_ids = _.get_nodes_by_type(Schema__MGraph__RAG__Node__Entity)
            for entity_node_id in entities_nodes_ids:
                entity_node  = data.node(entity_node_id)
                entity_name  =  entity_node.node_data.value
                entity_links = []
                for edge_id in _.get_node_outgoing_edges(entity_node):
                    entity_edge            = data.edge(edge_id)
                    entity_edge__outgoing = entity_edge.edge_label.outgoing
                    entity_edge__to_node_id = entity_edge.to_node_id()
                    entity_edge__to_node    = data.node(entity_edge__to_node_id)

                    if entity_edge__to_node.node_type  is Schema__MGraph__RAG__Node__Entity:
                        entity_links.append(dict(link_type   = entity_edge__outgoing               ,
                                                 entity_name = entity_edge__to_node.node_data.value))
                if entity_links:
                    entity_data  = obj(dict(entity_name  = entity_name,
                                            entity_links = entity_links))
                    entities.append(entity_data)

        with self.builder() as _:
            _.add_node(node_type=Node_Type__Article_Id, value=article_id)
            for entity in entities:
                kwargs_entity_node = dict(value     =  entity.entity_name,
                                          predicate = 'article_entity'           ,
                                          node_type = Node_Type__Entity  )
                _.add_connected_node(**kwargs_entity_node)
                for entity_link in entity.entity_links:
                    kwargs_linked_node = dict(value     = entity_link.entity_name,
                                              predicate = entity_link.link_type  ,
                                              node_type = Node_Type__Entity)
                    _.add_connected_node(**kwargs_linked_node).up()
                _.up()

        #self.mgraph_entities.print()

        #pprint(mgraph_text_entities.index().index_data.json())
        #pprint(mgraph_text_entities.index().values_index.json())

        return 'will go gere'

    @cache_on_self
    def builder(self):
        return self.mgraph_entities.builder()

    @cache_on_self
    def screenshot(self):
        return self.mgraph_entities.screenshot()

    def screenshot__setup(self):
        with self.screenshot().export().export_dot() as _:
            color__article_id = '#B0E0E6'  # Powder Blue - for Article ID nodes
            color__entity     = '#7EB36A'  # Sage Green - for entity nodes
            _.show_node__value()
            #_.show_node__type ()
            #_.show_node__id   ()
            _.show_edge__predicate()
            _.set_node__shape__type__box().set_node__shape__rounded()
            _.set_graph__splines__polyline()
            #_.set_graph__rank_dir__lr()
            #_.set_graph__layout_engine__fdp()
            #_.set_graph__layout_engine__circo()
            _.set_node__type_fill_color(node_type=Node_Type__Article_Id, color=color__article_id)
            _.set_node__type_fill_color(node_type=Node_Type__Entity    , color=color__entity)
            _.set_node__font__size(20)
            _.set_node__font__name('Arial')
        return self

    def png_bytes__for_mgraph_entities(self):
        png_bytes = self.screenshot__setup().screenshot().dot()
        return png_bytes

    def png_bytes__for_article__text_entities__description(self, article_entities: Hacker_News__Article__Entities) -> MGraph:
        png_bytes = article_entities.file___text__entities__description__png().load()
        return png_bytes

    def png_bytes__for_article__text_entities__title(self, article_entities: Hacker_News__Article__Entities) -> MGraph:
        png_bytes = article_entities.file___text__entities__title__png().load()
        return png_bytes

    def mgraph__for_article__text_entities__title(self, article_entities: Hacker_News__Article__Entities) -> MGraph:
        json_data = article_entities.file___text__entities__title__mgraph().load()
        if json_data:
            return MGraph.from_json(json_data)

    def mgraph__for_article__text_entities__description(self, article_entities: Hacker_News__Article__Entities) -> MGraph:
        json_data = article_entities.file___text__entities__description__mgraph().load()
        if json_data:
            return MGraph.from_json(json_data)

    def setup(self):
        self.file_articles_current.load()                           # load current articles data
        return self