from unittest                                                           import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Personas                     import My_Feeds__Personas
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage            import My_Feeds__Personas__Storage
from myfeeds_ai.personas.config.Config__My_Feeds__Personas import FILE_ID__PERSONA__CONNECTED__ENTITIES, \
    FILE_ID__PERSONA
from myfeeds_ai.personas.files.My_Feeds__Personas__File                 import My_Feeds__Personas__File
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                 import Schema__Persona__Types
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_local_stack


class test_My_Feeds__Personas(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.personas = My_Feeds__Personas()

    def test__init__(self):
        with self.personas as _:
            assert type(_)         is My_Feeds__Personas
            assert type(_.storage) is My_Feeds__Personas__Storage

    def test_files_in__latest(self):
        with self.personas as _:
            _.files_in__latest()

    def test_files_in__now(self):
        with self.personas as _:
            _.files_in__now()

    def test_file__llm_connect_entities(self):
        persona_type = Schema__Persona__Types.PRIVATE__CISO
        with self.personas.file__llm_connect_entities(persona_type=persona_type) as _:
            assert type(_)     is My_Feeds__Personas__File
            assert _.file_id   == f'{Schema__Persona__Types.PRIVATE__CISO.value}__{FILE_ID__PERSONA__CONNECTED__ENTITIES}'
            assert _.data_type is Schema__Persona__LLM__Connect_Entities


    def test_file__persona(self):
        persona_type = Schema__Persona__Types.TEAM__GRC
        with self.personas.file__persona(persona_type=persona_type) as _:
            assert type(_)         is My_Feeds__Personas__File
            assert _.file_id       == 'team-grc__persona'
            assert _.path_latest() == f'latest/{Schema__Persona__Types.TEAM__GRC.value}__{FILE_ID__PERSONA}.json'
            assert _.path_now   () == f'{_.folder__path_now()}/{Schema__Persona__Types.TEAM__GRC.value}__{FILE_ID__PERSONA}.json'

    def test_persona__description__png(self):
        with self.personas as _:
            persona_type = Schema__Persona__Types.EXEC__CISO
            png_bytes = _.persona__description__png(persona_type)
            if png_bytes:
                assert png_bytes.startswith(b'\x89PNG\r\n\x1a\n')

    def test_persona__description__tree_values(self):
        with self.personas as _:
            persona_type = Schema__Persona__Types.EXEC__CISO
            tree_values  = _.persona__description__tree_values(persona_type)
            if tree_values:
                assert type(tree_values) is str
            


