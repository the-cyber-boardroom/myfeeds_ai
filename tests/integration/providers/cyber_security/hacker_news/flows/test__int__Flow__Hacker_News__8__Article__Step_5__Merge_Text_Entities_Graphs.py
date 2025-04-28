from unittest                                                                                                                import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs import Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs
from tests.integration.data_feeds__objs_for_tests                                                                            import myfeeds_tests__setup_local_stack


class test__int__Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_llm_merge_text_entities_graphs = Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs()

    def test_task__1__load_articles_to_process(self):
        with self.flow_llm_merge_text_entities_graphs as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process      == _.file_articles_current.next_step__5__merge_text_entities_graphs()
            assert len(_.articles_to_process) >=  0

    def test_task__2__llm__create_text_entities_graphs(self):
        with self.flow_llm_merge_text_entities_graphs as _:
            _.max_graphs_to_merge = 4
            _.task__1__load_articles_to_process         ()
            _.task__2__llm__merge_text_entities_graphs ()

            # from osbot_utils.utils.Dev import pprint
            #pprint(_.status_changes.json())