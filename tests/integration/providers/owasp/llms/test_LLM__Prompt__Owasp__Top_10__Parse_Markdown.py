import pytest
from unittest                                                                                           import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache          import Hacker_News__Execute_LLM__With_Cache
from myfeeds_ai.providers.cyber_security.owasp.actions.Owasp__Files__Top_10                             import Owasp__Files__Top_10
from myfeeds_ai.providers.cyber_security.owasp.llms.prompts.LLM__Prompt__Owasp__Top_10__Parse_Markdown  import LLM__Prompt__Owasp__Top_10__Parse_Markdown
from myfeeds_ai.providers.cyber_security.owasp.schemas.Schema__Owasp__Top_10__Category                  import Schema__Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category                          import Owasp__Top_10__Category
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                                       import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                                              import Schema__LLM_Response
from osbot_utils.utils.Env                                                                              import get_env
from tests.integration.data_feeds__objs_for_tests                                                       import myfeeds_tests__setup_local_stack

class test_LLM__Prompt__Owasp__Top_10__Parse_Markdown(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        #load_dotenv()
        cls.owasp_files_top_10      = Owasp__Files__Top_10()
        cls.category                = Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL
        cls.category_markdown       = cls.owasp_files_top_10.raw_data(cls.category)
        cls.prompt_extract_category = LLM__Prompt__Owasp__Top_10__Parse_Markdown()
        cls.execute_llm_with_cache  = Hacker_News__Execute_LLM__With_Cache().setup()

    def test_llm_request(self):
        with self.prompt_extract_category as _:
            llm_request = _.llm_request(self.category_markdown)

            llm_response = self.execute_llm_with_cache.execute__llm_request(llm_request)
            if llm_response:
                owasp_top_10_category = _.process_llm_response(llm_response)
                assert type(llm_response)          is Schema__LLM_Response
                assert type(owasp_top_10_category) is Schema__Owasp__Top_10__Category




