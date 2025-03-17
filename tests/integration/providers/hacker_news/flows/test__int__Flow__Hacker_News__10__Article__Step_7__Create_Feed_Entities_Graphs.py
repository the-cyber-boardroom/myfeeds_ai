from unittest                                                                                                                    import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_MGraphs  import Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_MGraphs
from tests.integration.data_feeds__objs_for_tests                                                                                import myfeeds_tests__setup_local_stack


class test__int__Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_Graphs(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_llm_create_feed_entities_graphs = Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_MGraphs()

    def test_task__1__load_articles_to_process(self):
        with self.flow_llm_create_feed_entities_graphs as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process == _.file_articles_current.next_step__7__merge_day_entities_graphs()
            assert len(_.articles_to_process) >= 0
            #pprint(_.articles_to_process)

    def test_task__2__create_file_with_feed_text_entities_mgraph(self):
        with self.flow_llm_create_feed_entities_graphs as _:
            _.max_articles_to_process = 1
            _.task__1__load_articles_to_process                  ()
            _.task__2__create_file_with_feed_text_entities_mgraph()
            _.task__3__move_articles_to_next_step                ()
            _.task__4__create_output                             ()

            #pprint(_.output)

            # file_size 295355
            # files_to_process 50
            #
            # title:      : {'edges_ids': 767, 'nodes_ids': 321}
            # description : {'edges_ids': 799, 'nodes_ids': 367}
            # both        : {'edges_ids': 1451, 'nodes_ids': 553}

    # def test_task__3__create_png_for_feed_text_entities_mgraph(self):
    #     with self.flow_llm_create_feed_entities_graphs as _:
    #         _.task__3__create_png_for_feed_text_entities_mgraph()
    #
    #         # {'edges_ids': 733, 'nodes_ids': 305}
    #         # {'edges_ids': 1451, 'nodes_ids': 553} - "create png" took: 222.159 seconds - looked good but it is not usable



