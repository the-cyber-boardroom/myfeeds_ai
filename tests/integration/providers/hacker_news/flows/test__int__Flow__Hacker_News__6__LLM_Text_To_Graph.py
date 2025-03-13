from unittest                                                                                      import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__6__LLM_Text_To_Graph import Flow__Hacker_News__6__LLM_Text_To_Graph
from tests.integration.data_feeds__objs_for_tests                                                  import myfeeds_tests__setup_local_stack

class test__int__Flow__Hacker_News__6__LLM_Text_To_Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_llm_text_to_graph = Flow__Hacker_News__6__LLM_Text_To_Graph()

    def test_task__1__load_articles_to_process(self):
        with self.flow_llm_text_to_graph as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process      == _.file_articles_current.next_step__3__llm_text_to_graph()
            assert len(_.articles_to_process) >=  0

    def test_task__2__llm__text_to_graph(self):
        with self.flow_llm_text_to_graph as _:
            _.task__1__load_articles_to_process()
            _.task__2__llm__text_to_graph      ()

            #pprint(_.status_changes.json())

