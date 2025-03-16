import pytest
from unittest                                                                                                           import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Entities  import Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Entities
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                                                       import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Env                                                                                              import get_env
from tests.integration.data_feeds__objs_for_tests                                                                       import myfeeds_tests__setup_local_stack

class test__int__Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_llm_text_to_graph = Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Entities()

    def test_task__1__load_articles_to_process(self):
        with self.flow_llm_text_to_graph as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process      == _.file_articles_current.next_step__3__llm_text_to_entities()
            assert len(_.articles_to_process) >=  0

    def test_task__2__llm__text_to_graph(self):
        with self.flow_llm_text_to_graph as _:
            _.max_articles_to_create = 2
            _.task__1__load_articles_to_process()
            _.task__2__llm__text_to_graph      ()

            # from osbot_utils.utils.Dev import pprint
            # pprint(_.status_changes.json())


    # def test_parallel_execution_test(self):
    #     import concurrent
    #     from time import sleep
    #     from osbot_utils.utils.Http import GET
    #
    #     def wait_for(seconds):
    #         with print_duration():
    #             if seconds and seconds > 0:
    #                 sleep(seconds)
    #
    #             http = GET("https://www.thecyberboardroom.com/")
    #             return f"Waited for {seconds} seconds and got {len(http)} page"
    #
    #     def concurrency_test_parallel():
    #         print('starting parallel execution')
    #
    #         # Create a thread pool
    #
    #         with concurrent.futures.ThreadPoolExecutor() as executor:
    #             # Submit both wait operations to run in parallel
    #             future1 = executor.submit(wait_for, 1)
    #             future2 = executor.submit(wait_for, 1)
    #
    #             # Wait for both to complete
    #             result1 = future1.result()
    #             result2 = future2.result()
    #
    #         print('all operations completed')
    #         print(result1)
    #         print(result2)
    #
    #     # Running the test
    #     with print_duration():
    #         concurrency_test_parallel()

