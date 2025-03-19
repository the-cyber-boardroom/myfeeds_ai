from unittest                                                           import TestCase
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                import S3_Key__File_Extension
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage__Persona   import My_Feeds__Personas__Storage__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Types                 import Schema__Persona__Types
from osbot_utils.helpers.Safe_Id                                        import Safe_Id

class test_My_Feeds__Personas__Storage__Persona(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.persona_type    = Schema__Persona__Types.PUBLIC__BOARD_MEMBER
        cls.persona_storage = My_Feeds__Personas__Storage__Persona(persona_type=cls.persona_type)

    def test__init__(self):
        with self.persona_storage as _:
            assert type(_) == My_Feeds__Personas__Storage__Persona
            folder_now  = _.path__folder_now()
            file_id     = Safe_Id()
            extension   = S3_Key__File_Extension.JSON
            path_latest = _.path__latest(file_id=file_id, extension=extension)
            path_now    = _.path__now   (file_id=file_id, extension=extension)
            assert path_latest                                  == f'latest/{file_id}.json'
            assert path_now                                     == f'{folder_now}/{file_id}.json'
            assert f'public-data/personas/{path_now}'           == _.s3_db.s3_key__for_provider_path(s3_path=path_now)
            assert folder_now.endswith(self.persona_type.value) is True

