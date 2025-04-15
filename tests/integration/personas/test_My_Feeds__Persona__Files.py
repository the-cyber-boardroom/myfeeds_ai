from unittest                                                                   import TestCase

import pytest

from myfeeds_ai.personas.actions.My_Feeds__Persona__Files                       import My_Feeds__Persona__Files
from myfeeds_ai.personas.config.Config__My_Feeds__Personas                      import FILE_ID__PERSONA, FILE_ID__PERSONA__ARTICLES__CONNECTED__ENTITIES
from myfeeds_ai.personas.files.My_Feeds__Personas__File                         import My_Feeds__Personas__File
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now                    import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.schemas.Schema__Persona__Articles__Connected_Entities  import Schema__Persona__Articles__Connected_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from osbot_utils.utils.Env import in_github_action
from tests.integration.data_feeds__objs_for_tests                               import myfeeds_tests__setup_local_stack

class test_My_Feeds__Persona__Files(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.persona_files = My_Feeds__Persona__Files()

    def test_file__persona_articles__connected_entities(self):
        persona_type = Schema__Persona__Types.PRIVATE__CISO
        with self.persona_files.file__persona_articles__connected_entities(persona_type=persona_type) as _:
            assert type(_)     is My_Feeds__Personas__File__Now
            assert _.file_id   == FILE_ID__PERSONA__ARTICLES__CONNECTED__ENTITIES
            assert _.data_type is Schema__Persona__Articles__Connected_Entities


    def test_file__persona(self):
        persona_type = Schema__Persona__Types.TEAM__GRC
        with self.persona_files.file__persona(persona_type=persona_type) as _:
            assert type(_)         is My_Feeds__Personas__File
            assert _.file_id       == 'persona'
            assert _.path_latest() == f'latest/{Schema__Persona__Types.TEAM__GRC.value}__{FILE_ID__PERSONA}.json'
            assert _.path_now   () == f'{_.folder__path_now()}/{FILE_ID__PERSONA}.json'

    def test_persona__description__png(self):
        if in_github_action():
            pytest.skip("Test needs aws access")
        with self.persona_files as _:
            persona_type = Schema__Persona__Types.EXEC__CISO
            png_bytes = _.persona__description__png(persona_type)
            if png_bytes:
                assert png_bytes.startswith(b'\x89PNG\r\n\x1a\n')