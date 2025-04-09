from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File_Extension
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage                    import My_Feeds__Personas__Storage
from myfeeds_ai.personas.config.Config__My_Feeds__Personas                      import FILE_ID__PERSONA__CONNECTED__ENTITIES, FILE_ID__PERSONA, FILE_ID__PERSONA__DIGEST
from myfeeds_ai.personas.files.My_Feeds__Personas__File                         import My_Feeds__Personas__File
from myfeeds_ai.personas.llms.Schema__Persona__Digest                           import Schema__Persona__Digest
from myfeeds_ai.personas.schemas.Schema__Persona                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities         import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from osbot_utils.helpers.Safe_Id                                                import Safe_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe

class My_Feeds__Personas(Type_Safe):
    storage : My_Feeds__Personas__Storage

    @type_safe
    def files_in__now(self, include_sub_folders:bool = True):
        return self.storage.files_in__now(include_sub_folders=include_sub_folders)

    @type_safe
    def files_in__latest(self):
        return self.storage.files_in__latest()


