from unittest                                                                                                               import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs import Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs
from tests.integration.data_feeds__objs_for_tests                                                                           import myfeeds_tests__setup_local_stack


class test__int__Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_llm_merge_day_entities_graphs = Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs()

    def test_task__1__load_articles_to_process(self):
        with self.flow_llm_merge_day_entities_graphs as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process      == _.file_articles_current.next_step__6__merge_day_entities_graphs()
            assert len(_.articles_to_process) >=  0

    def test_task__4__create_mgraph_png(self):
        with self.flow_llm_merge_day_entities_graphs as _:
            _.max_graphs_to_merge = 1
            _.task__1__load_articles_to_process       ()
            _.task__2__find_days_to_process           ()
            _.task__3__llm__merge_day_entities_graphs ()
            _.task__4__create_mgraph_png              ()
            _.task__5__update_file_articles           ()
            _.task__6__create_output                  ()

            # from osbot_utils.utils.Dev import pprint
            # pprint(_.status_changes.json())
            # pprint(_.output)
