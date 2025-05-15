from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph                          import Html_MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Screenshot              import Schema__Html_MGraph__Screenshot__Config
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Nodes   import Schema__Html_MGraph__Node__HTML__BODY
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe


class Html_MGraph__View__Page_Structure(Type_Safe):
    html_mgraph : Html_MGraph
    create_png  : bool = False

    def create_screenshot(self):
        if self.create_png:
            with Schema__Html_MGraph__Screenshot__Config() as _:
                _.target_file          = f"{self.__class__.__name__}.png"
                #_.graph.title          = self.title
                #_.graph.layout_engine = MGraph__Export__Dot__Layout__Engine.FDP
                _.print_dot_code      = False
                #_.graph.node_sep       = 0.1
                #_.graph.rank_sep        = 0.1
                #_.graph.spring_constant = 0.25
                self.html_mgraph.html_mgraph__screenshot().create(config=_)

    def create_using_mquery(self):
        png_path = 'create_using_mquery.png'

        # with self.html_mgraph.query().mgraph_index as _:
        #     _.print()

        with self.html_mgraph.query() as _:
            _.add().add_nodes_with_type(Schema__Html_MGraph__Node__HTML__BODY)
            #html_node_ids = _.mgraph_index.get_nodes_by_type(Schema__Html_MGraph__Node__HTML__DIV)
            #_.add_nodes_ids(html_node_ids)

            #pprint(html_node_ids)
            #_.by_type(Schema__Html_MGraph__Node__HTML__HTML)
            #
            _.add_outgoing_edges__with_depth(2)
            # with _.navigate() as navigate:
            #     navigate.to_connected_nodes()


            # _.print_stats()
            # #_.save_to_png(path=png_path, show_source_graph=False)
            # mgraph_view = _.export_view()
            # html_mgraph = Html_MGraph(graph=mgraph_view)
            # config = Html_MGraph__Screenshot__Config(target_file='roundtrip.png')
            # html_mgraph.html_mgraph__screenshot().create(config)