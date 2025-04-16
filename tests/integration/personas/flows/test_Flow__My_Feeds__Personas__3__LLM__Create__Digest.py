import pytest
from unittest                                                                   import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Persona                              import My_Feeds__Persona
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__3__LLM__Create__Digest import Flow__My_Feeds__Personas__3__LLM__Create__Digest
from myfeeds_ai.personas.schemas.Schema__Persona                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Articles__Connected_Entities  import Schema__Persona__Articles__Connected_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI               import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Env                                                      import get_env
from tests.integration.data_feeds__objs_for_tests                               import myfeeds_tests__setup_local_stack


class test_Flow__My_Feeds__Personas__3__LLM__Create__Digest(TestCase):
    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.persona_type       = Schema__Persona__Types.EXEC__CISO
        cls.flow_create_digest = Flow__My_Feeds__Personas__3__LLM__Create__Digest(persona_type=cls.persona_type)

    def test_task__1__load_persona_data(self):
        with self.flow_create_digest as _:
            _.task__1__load_persona_data()
            assert type(_.persona                   ) is My_Feeds__Persona
            assert type(_.persona_type              ) is Schema__Persona__Types
            assert _.persona_type                     == Schema__Persona__Types.EXEC__CISO
            assert type(_.persona_data              ) is Schema__Persona
            assert type(_.persona_connected_entities) is Schema__Persona__Articles__Connected_Entities

    # def test_task__2__llm_create_persona_digest(self):
    #     with self.flow_create_digest as _:
    #         _.task__1__load_persona_data()
    #         _.task__2__llm_create_persona_digest()
    #         assert type(_.persona_digest_articles) is Schema__Persona__Digest_Articles

    def test_task__3__save_persona_digest(self):
        with self.flow_create_digest as _:
            _.task__1__load_persona_data        ()
            _.task__2__llm_create_persona_digest()
            _.task__3__save_persona_digest      ()

            #pprint(_.persona.data().json())

    # def test_task__4__create_output(self):
    #     with self.flow_create_digest as _:
    #         _.task__1__load_persona_data        ()
    #         _.task__2__llm_create_persona_digest()
    #         _.task__3__save_persona_digest      ()
    #         _.task__4__create_output            ()
    #
    #         from osbot_utils.utils.Dev import pprint
    #         pprint(_.output)

