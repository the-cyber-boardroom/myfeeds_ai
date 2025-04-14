from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                import S3_Key__File__Extension, S3_Key__File__Content_Type
from myfeeds_ai.personas.config.Config__My_Feeds__Personas              import FILE_ID__PERSONA__CONNECTED__ENTITIES, FILE_ID__PERSONA__DIGEST, FILE_ID__PERSONA, FILE_ID__PERSONA__ENTITIES
from myfeeds_ai.personas.files.My_Feeds__Personas__File                 import My_Feeds__Personas__File
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now            import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.llms.Schema__Persona__Digest                   import Schema__Persona__Digest
from myfeeds_ai.personas.schemas.Schema__Persona                        import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Text__Entities        import Schema__Persona__Text__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                 import Schema__Persona__Types
from osbot_utils.helpers.Safe_Id                                        import Safe_Id
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                         import type_safe

# todo: I think a better name for this class is My_Feeds__Persona__Files
class My_Feeds__Persona__Data(Type_Safe):

    @type_safe
    def file__persona(self, persona_type: Schema__Persona__Types):
        kwargs_file= dict(persona_type = persona_type                ,
                          file_id      = FILE_ID__PERSONA            ,
                          extension    = S3_Key__File__Extension.JSON,
                          data_type    = Schema__Persona             )
        return My_Feeds__Personas__File(**kwargs_file)


    @type_safe
    def file__persona_connect_entities(self, persona_type: Schema__Persona__Types):
        file_id = Safe_Id(persona_type.value + '__' + FILE_ID__PERSONA__CONNECTED__ENTITIES)
        kwargs_file= dict(persona_type = persona_type,
                          file_id      = file_id,
                          extension    = S3_Key__File__Extension.JSON,
                          data_type    = Schema__Persona__LLM__Connect_Entities)
        return My_Feeds__Personas__File(**kwargs_file)

    @type_safe
    def file__persona_digest(self, persona_type: Schema__Persona__Types):
        file_id = Safe_Id(persona_type.value + '__' + FILE_ID__PERSONA__DIGEST)
        kwargs_file= dict(persona_type = persona_type,
                          file_id      = file_id,
                          extension    = S3_Key__File__Extension.JSON,
                          data_type    = Schema__Persona__Digest)
        return My_Feeds__Personas__File(**kwargs_file)

    @type_safe
    def file__persona_entities(self, persona_type: Schema__Persona__Types):
        kwargs_file = dict(persona_type = persona_type                      ,
                           file_id      = FILE_ID__PERSONA__ENTITIES        ,
                           extension    = S3_Key__File__Extension.JSON      ,
                           data_type    = Schema__Persona__Text__Entities   )
        return My_Feeds__Personas__File__Now(**kwargs_file)

    @type_safe
    def file__persona_entities__png(self, persona_type: Schema__Persona__Types):
        kwargs_file = dict(persona_type = persona_type                  ,
                           file_id      = FILE_ID__PERSONA__ENTITIES    ,
                           extension    = S3_Key__File__Extension.PNG   ,
                           content_type = S3_Key__File__Content_Type.PNG)
        return My_Feeds__Personas__File__Now(**kwargs_file)

    @type_safe
    def file__persona_entities__tree_values(self, persona_type: Schema__Persona__Types):
        kwargs_file = dict(persona_type = persona_type                   ,
                           file_id      = FILE_ID__PERSONA__ENTITIES     ,
                           extension    = S3_Key__File__Extension.TXT    ,
                           content_type = S3_Key__File__Content_Type.TXT )
        return My_Feeds__Personas__File__Now(**kwargs_file)

    # todo: needs fixing so that we don't use: persona_type.value + '__' + FILE_ID__PERSONA__DIGEST
    @type_safe
    def file__persona_digest_html(self, persona_type: Schema__Persona__Types):
        file_id = Safe_Id(persona_type.value + '__' + FILE_ID__PERSONA__DIGEST)
        kwargs_file= dict(persona_type = persona_type,
                          file_id      = file_id,
                          extension    = S3_Key__File__Extension.HTML   ,
                          content_type = S3_Key__File__Content_Type.HTML,
                          data_type    = Schema__Persona__Digest        )
        return My_Feeds__Personas__File(**kwargs_file)

    #todo: refactor this into a method that is able to get the file contents of the file_persona.path__** files
    def persona__description__png(self, persona_type: Schema__Persona__Types):
        file_persona                   = self.file__persona(persona_type)
        path__persona__entities__png = file_persona.data().path__persona__entities__png
        kwargs = dict(s3_path        = path__persona__entities__png  ,
                      content_type   = S3_Key__File__Content_Type.TXT)
        return file_persona.hacker_news_storage.path__load_data(**kwargs)

        # file_persona           = self.file__persona(persona_type)
        # persona                = file_persona.data()
        # if persona.path__description__png:
        #     return file_persona.hacker_news_storage.path__load_bytes(persona.path__description__png)
        # else:
        #     persona.path__description__png = persona.path_now.replace(S3_Key__File__Extension.JSON.value, S3_Key__File__Extension.PNG.value)
        #
        # text_entities = persona.description__entities
        # if text_entities:
        #     from myfeeds_ai.personas.actions.My_Feeds__Personas__Create import My_Feeds__Personas__Create
        #     personas_create = My_Feeds__Personas__Create()
        #     graph_rag       = personas_create.prompt_extract_entities.create_entities_graph_rag(text_entities)
        #     bytes_png       = graph_rag.screenshot__create_bytes()
        #     save_kwargs = dict(path=persona.path__description__png, data=bytes_png, content_type = S3_Key__File__Content_Type.PNG)
        #     file_persona.hacker_news_storage.path__save_bytes(**save_kwargs)
        #
        #     file_persona.save_data(persona.json())
        #     return bytes_png


    def persona__description__tree_values(self, persona_type: Schema__Persona__Types):
        file_persona                         = self.file__persona(persona_type)
        path__persona__entities__tree_values = file_persona.data().path__persona__entities__tree_values
        kwargs = dict(s3_path      = path__persona__entities__tree_values,
                      content_type = S3_Key__File__Content_Type.TXT      )
        return file_persona.hacker_news_storage.path__load_data(**kwargs)
