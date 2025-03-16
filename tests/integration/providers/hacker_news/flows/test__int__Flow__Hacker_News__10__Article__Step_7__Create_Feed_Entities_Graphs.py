from unittest                                                                                                                   import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_Graphs  import Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_Graphs
from tests.integration.data_feeds__objs_for_tests                                                                               import myfeeds_tests__setup_local_stack


class test__int__Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_Graphs(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_llm_create_feed_entities_graphs = Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_Graphs()

    def test_task__1__load_articles_to_process(self):
        with self.flow_llm_create_feed_entities_graphs as _:
            _.task__1__load_articles_to_process()
            assert len(_.articles_to_process.articles) >= 0

