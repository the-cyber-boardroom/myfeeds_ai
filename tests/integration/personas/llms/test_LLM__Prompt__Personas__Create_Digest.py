import pytest
from unittest                                                                                   import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Personas                                             import My_Feeds__Personas
from myfeeds_ai.personas.llms.LLM__Prompt__Personas__Create_Digest                              import LLM__Prompt__Personas__Create_Digest, SYSTEM_PROMPT__CREATE_DIGEST, USER_PROMPT__CREATE_DIGEST
from myfeeds_ai.personas.llms.Schema__Persona__Digest                                           import Schema__Persona__Digest
from myfeeds_ai.personas.schemas.Schema__Persona                                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities                         import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                                         import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache  import Hacker_News__Execute_LLM__With_Cache
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                               import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role                        import Schema__LLM_Request__Message__Role
from osbot_utils.utils.Dev                                                                      import pprint
from osbot_utils.utils.Env                                                                      import get_env
from osbot_utils.utils.Files                                                                    import file_create
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack


class test_LLM__Prompt__Personas__Create_Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.prompt_create_digest       = LLM__Prompt__Personas__Create_Digest()
        cls.persona_type               = Schema__Persona__Types.EXEC__CEO
        cls.personas                   = My_Feeds__Personas()
        cls.persona                    = cls.personas.file__persona             (persona_type=cls.persona_type).data()
        cls.persona_connected_entities = cls.personas.file__llm_connect_entities(persona_type=cls.persona_type).data()

    def test_format_articles_content(self):                          # Test that article content is correctly formatted.
        if self.persona:
            assert type(self.persona) is Schema__Persona
            assert type(self.persona_connected_entities) is Schema__Persona__LLM__Connect_Entities
            formatted_content = self.prompt_create_digest.format_articles_content(self.persona_connected_entities)

            assert "ARTICLE"  in formatted_content
            assert "Author"  in formatted_content
            assert "-----"   in formatted_content                               # Check separator

    def test_format_connected_entities_data(self):                              # Test that connected entities data is correctly formatted.
        formatted_data = self.prompt_create_digest.format_connected_entities_data(self.persona_connected_entities)

        assert "ARTICLE ID:"              in formatted_data
        assert "PRIMARY RELEVANCE AREAS:" in formatted_data

    def test_llm_request(self):                                                 # Test that the LLM request is properly formatted.
        llm_request = self.prompt_create_digest.llm_request(persona                     = self.persona                   ,
                                                            persona_connected_entities  = self.persona_connected_entities)
        assert llm_request.request_data.function_call.parameters == Schema__Persona__Digest         # Check function call parameters

        with llm_request.request_data.messages[0] as _:                                             # Check system message
            assert _.role    == Schema__LLM_Request__Message__Role.SYSTEM
            assert _.content == SYSTEM_PROMPT__CREATE_DIGEST


        with llm_request.request_data.messages[1] as _:                                                                 # Check user message
            assert _.role                                             == Schema__LLM_Request__Message__Role.USER
            assert self.persona.description                           in  _.content                                     # Check that the persona description is included
            assert f"PERSONA TYPE: {self.persona.persona_type.value}" in  _.content                                     # Check that persona type is included
            assert "ARTICLE ID: "                                     in  _.content                                     # Check that formatted connected entities data is included
            assert "RELEVANCE SCORE: "                                in  _.content


    def test_process_llm_response(self):    # Test processing an LLM response into a structured digest.
        llm_request = self.prompt_create_digest.llm_request(persona                     = self.persona                   ,
                                                            persona_connected_entities  = self.persona_connected_entities)

        with Hacker_News__Execute_LLM__With_Cache().setup() as _:
            # _.refresh_llm_cache()
            llm_response = _.execute__llm_request(llm_request)

        digest = self.prompt_create_digest.process_llm_response(llm_response)


        pprint(digest.json())
        file_create(path='./digest.html', contents=digest.get_html())

        # todo: fix and improve the asserts below
        self.assertIsInstance(digest, Schema__Persona__Digest)                  # Verify the result is a proper Schema__Persona__Digest

        # Check that required fields are present
        self.assertTrue(hasattr(digest, 'persona_type'))
        self.assertTrue(hasattr(digest, 'executive_summary'))
        self.assertTrue(hasattr(digest, 'articles'))
        self.assertTrue(hasattr(digest, 'strategic_implications'))

        self.assertGreater(len(digest.articles), 0)                             # Check that there are articles in the digest


        self.assertEqual(digest.persona_type, self.persona_type.value)          # Check that persona type is correctly set

        for article in digest.articles:                                         # Check article structure
            self.assertTrue(hasattr(article, 'article_id'            ))
            self.assertTrue(hasattr(article, 'headline'              ))
            self.assertTrue(hasattr(article, 'summary'               ))
            self.assertTrue(hasattr(article, 'relevance_analysis'    ))
            self.assertTrue(hasattr(article, 'action_recommendations'))
            self.assertTrue(hasattr(article, 'priority_level'        ))