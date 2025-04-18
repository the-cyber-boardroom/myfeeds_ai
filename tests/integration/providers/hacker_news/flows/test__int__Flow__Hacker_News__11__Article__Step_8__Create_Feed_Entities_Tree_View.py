from unittest                                                                                                                       import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View   import Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View
from tests.integration.data_feeds__objs_for_tests                                                                                   import myfeeds_tests__setup_local_stack


class test__int__Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_llm_create_feed_entities_graphs = Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View()

    def test_task__1__load_articles_to_process(self):
        with self.flow_llm_create_feed_entities_graphs as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process == _.file_articles_current.next_step__8__create_feed_entities_tree_view()
            assert len(_.articles_to_process) >= 0
            # from osbot_utils.utils.Dev import pprint
            # pprint(_.articles_to_process)

    def test_task__2__create_file_with_feed_text_entities_mgraph(self):
        with self.flow_llm_create_feed_entities_graphs as _:
            _.max_articles_to_load = 5
            _.task__1__load_articles_to_process                     ()
            _.task__2__create_file_with_feed_text_entities_tree_view()
            _.task__3__update__feed_text_entities__files            ()
            _.task__4__move_articles_to_next_step                   ()
            _.task__5__create_output                                ()


            #from osbot_utils.utils.Dev import pprint
            #pprint(_.output)