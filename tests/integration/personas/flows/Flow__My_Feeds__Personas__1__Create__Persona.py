import pytest
from unittest                                                               import TestCase
from myfeeds_ai.personas.config.Config__My_Feeds__Personas                  import FILE_ID__PERSONA
from myfeeds_ai.personas.files.My_Feeds__Personas__File                     import My_Feeds__Personas__File
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__1__Create__Persona import Flow__My_Feeds__Personas__1__Create__Persona
from myfeeds_ai.personas.schemas.Schema__Persona                            import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Entities                  import Schema__Persona__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                     import Schema__Persona__Types
from osbot_utils.helpers.Obj_Id                                             import Obj_Id
from osbot_utils.helpers.Safe_Id                                            import Safe_Id
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI           import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Env                                                  import get_env
from tests.integration.data_feeds__objs_for_tests                           import myfeeds_tests__setup_local_stack


class Flow__My_Feeds__Personas__1__Create__Persona(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.flow_create_persona = Flow__My_Feeds__Personas__1__Create__Persona()

    def test_task__1__load_persona_data(self):
        with self.flow_create_persona as _:

            _.task__1__load_persona_data()
            assert type(_.file_persona        ) is My_Feeds__Personas__File
            assert type(_.persona             ) is Schema__Persona
            assert type(_.persona_type        ) is Schema__Persona__Types
            assert type(_.file_persona.file_id) is Safe_Id
            assert _.file_persona.file_id       == f"{_.persona_type.value}__{FILE_ID__PERSONA}"

    def test__2__set_persona_details(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data()
            _.test__2__set_persona_details()

    def test__3__set_persona_details(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data()
            _.test__3__create_entities()

            assert type(_.persona                                  ) is Schema__Persona
            assert type(_.persona.description__entities            ) is Schema__Persona__Entities
            assert type(_.persona.cache_ids['description-entities']) is Obj_Id

    def test_test__4__create_tree_values(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data()
            _.task__4__create_tree_values()

            assert type(_.persona.description__tree_values) is str
            assert len (_.persona.description__tree_values) > 10




