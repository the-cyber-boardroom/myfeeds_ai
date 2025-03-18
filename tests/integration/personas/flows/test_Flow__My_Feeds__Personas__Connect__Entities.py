import pytest
from unittest import TestCase

from myfeeds_ai.personas.files.My_Feeds__Personas__File                             import My_Feeds__Personas__File
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__LLM__Connect_Entities      import Flow__My_Feeds__Personas__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona                                    import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                             import Schema__Persona__Types
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                   import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env                                                          import get_env
from tests.integration.data_feeds__objs_for_tests                                   import myfeeds_tests__setup_local_stack


class test_Flow__My_Feeds__Personas__Connect__Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.flow_connect_entities = Flow__My_Feeds__Personas__LLM__Connect_Entities()

    def test_task__1__load_persona_data(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data()
            assert type(_.file_persona        ) is My_Feeds__Personas__File
            assert type(_.persona             ) is Schema__Persona
            assert type(_.persona_type        ) is Schema__Persona__Types
            assert type(_.file_persona.file_id) is Safe_Id
            assert _.file_persona.file_id       == _.persona_type.value

    def test_task__2__setup__file_llm_connect_entities(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data               ()
            _.task__2__setup__file_llm_connect_entities()
            _.task__n__create_output                   ()
            assert type(_.llm_connect_entities)      is Schema__Persona__LLM__Connect_Entities
            assert type(_.file_llm_connect_entities) is My_Feeds__Personas__File

            print(_.output)

