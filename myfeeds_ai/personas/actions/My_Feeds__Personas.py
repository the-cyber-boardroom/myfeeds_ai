from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File_Extension
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage                    import My_Feeds__Personas__Storage
from myfeeds_ai.personas.files.My_Feeds__Personas__File                         import My_Feeds__Personas__File
from myfeeds_ai.personas.schemas.Schema__Persona                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from osbot_utils.helpers.Safe_Id                                                import Safe_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe


class My_Feeds__Personas(Type_Safe):
    storage : My_Feeds__Personas__Storage

    @type_safe
    def file__persona(self, persona_type: Schema__Persona__Types):
        persona_id = Safe_Id(persona_type.value)
        kwargs_file= dict(file_id   = persona_id                 ,
                          extension = S3_Key__File_Extension.JSON,
                          data_type = Schema__Persona            )
        return My_Feeds__Personas__File(**kwargs_file)

    @type_safe
    def files_in__now(self, include_sub_folders:bool = True):
        return self.storage.files_in__now(include_sub_folders=include_sub_folders)

    @type_safe
    def files_in__latest(self):
        return self.storage.files_in__latest()

    # todo: see if this is really needed (and if so, see where it should be better place and solve the circular dependency)
    def persona__description__png(self, persona_type: Schema__Persona__Types):
        persona = self.file__persona(persona_type).data()
        text_entities = persona.description__entities
        if text_entities:
            from myfeeds_ai.personas.actions.My_Feeds__Personas__Create import My_Feeds__Personas__Create
            personas_create = My_Feeds__Personas__Create()
            graph_rag       = personas_create.prompt_extract_entities.create_entities_graph_rag(text_entities)
            return graph_rag.screenshot__create_bytes()

    def persona__description__tree_values(self, persona_type: Schema__Persona__Types):
        with self.file__persona(persona_type).data() as _:
            return _.description__tree_values



