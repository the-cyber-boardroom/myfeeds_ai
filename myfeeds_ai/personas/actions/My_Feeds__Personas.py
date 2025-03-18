from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File_Extension
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage                    import My_Feeds__Personas__Storage
from myfeeds_ai.personas.files.My_Feeds__Personas__File                         import My_Feeds__Personas__File
from myfeeds_ai.personas.schemas.Schema__Persona                                import Schema__Persona
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import FILE_ID__PERSONA__CISO
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                          import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe


class My_Feeds__Personas(Type_Safe):
    storage : My_Feeds__Personas__Storage

    def file__persona__ciso(self):
        return My_Feeds__Personas__File(file_id=FILE_ID__PERSONA__CISO, extension=S3_Key__File_Extension.JSON)

    def file__persona__ciso__load(self) -> Schema__Persona:
        with self.file__persona__ciso() as _:
            if _.exists():
                json_data = _.load()
                return Schema__Persona.from_json(json_data)
            else:
                return Schema__Persona()

    def persona__ciso(self):
        from myfeeds_ai.personas.actions.My_Feeds__Personas__Create import My_Feeds__Personas__Create
        personas_create = My_Feeds__Personas__Create()
        return personas_create.create_persona__ciso()

    @type_safe
    def files_in__now(self, include_sub_folders:bool = True):
        return self.storage.files_in__now(include_sub_folders=include_sub_folders)

    @type_safe
    def files_in__latest(self):
        return self.storage.files_in__latest()


