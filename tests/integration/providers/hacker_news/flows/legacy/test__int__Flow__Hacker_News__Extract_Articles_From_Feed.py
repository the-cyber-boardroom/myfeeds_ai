# from unittest                                                                                            import TestCase
# from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Extract_Articles_From_Feed import Flow__Hacker_News__Extract_Articles_From_Feed
# from osbot_utils.helpers.flows.Flow                                                                      import Flow
# from osbot_utils.utils.Dev import pprint
# from osbot_utils.utils.Objects import __
#
#
# class test__int__Flow__Hacker_News__Extract_Articles_From_Feed(TestCase):
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         from tests.integration.data_feeds__objs_for_tests import cbr_website__assert_local_stack
#         cbr_website__assert_local_stack()
#
#         cls.flow__extract_articles = Flow__Hacker_News__Extract_Articles_From_Feed()
#
#     def setUp(self):
#         self.flow = self.flow__extract_articles.flow__extract_articles_from_feed()
#
#     def tearDown(self):
#         self.flow.print_log_messages()
#
#     def test__init__(self):
#         with self.flow as _:
#             assert type(_) is Flow
#             assert _.flow_config.obj() == __(add_task_to_self          = True  ,
#                                              log_to_console            = False ,
#                                              log_to_memory             = True  ,
#                                              logging_enabled           = True  ,
#                                              print_logs                = False ,
#                                              print_none_return_value   = False ,
#                                              print_finished_message    = False ,
#                                              print_error_stack_trace   = False  ,
#                                              raise_flow_error          = True  ,
#                                              flow_data__capture_events = False )
#
#     def test_flow__extract_articles_from_feed(self):
#         with self.flow as _:
#             assert _.execute_flow()    == _
#
#             #_.print__flow_data()
#
