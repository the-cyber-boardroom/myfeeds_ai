from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                       import S3_Key__File__Extension, S3_Key__File__Content_Type
from myfeeds_ai.personas.config.Config__My_Feeds__Personas                     import FILE_ID__PERSONA__DIGEST, FILE_ID__PERSONA, FILE_ID__PERSONA__ENTITIES, FILE_ID__PERSONA__ARTICLES__CONNECTED__ENTITIES
from myfeeds_ai.personas.files.My_Feeds__Personas__File                        import My_Feeds__Personas__File
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now                   import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.llms.Schema__Persona__Digest                          import Schema__Persona__Digest
from myfeeds_ai.personas.schemas.Schema__Persona                               import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Articles__Connected_Entities import Schema__Persona__Articles__Connected_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Text__Entities               import Schema__Persona__Text__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                        import Schema__Persona__Types
from osbot_utils.type_safe.Type_Safe                                           import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                import type_safe

class My_Feeds__Persona__Files(Type_Safe):

    @type_safe
    def file__persona(self, persona_type: Schema__Persona__Types) -> My_Feeds__Personas__File:
        kwargs_file= dict(persona_type = persona_type                ,
                          file_id      = FILE_ID__PERSONA            ,
                          extension    = S3_Key__File__Extension.JSON,
                          data_type    = Schema__Persona             )
        return My_Feeds__Personas__File(**kwargs_file)

    @type_safe
    def file__persona_articles__connected_entities(self, persona_type: Schema__Persona__Types) ->My_Feeds__Personas__File__Now:
        kwargs_file = dict(persona_type = persona_type,
                           file_id      = FILE_ID__PERSONA__ARTICLES__CONNECTED__ENTITIES,
                           extension    = S3_Key__File__Extension.JSON,
                           data_type    = Schema__Persona__Articles__Connected_Entities)
        return My_Feeds__Personas__File__Now(**kwargs_file)

    @type_safe
    def file__persona_digest(self, persona_type: Schema__Persona__Types) -> My_Feeds__Personas__File:
        kwargs_file= dict(persona_type = persona_type,
                          file_id      = FILE_ID__PERSONA__DIGEST,
                          extension    = S3_Key__File__Extension.JSON,
                          data_type    = Schema__Persona__Digest)
        return My_Feeds__Personas__File(**kwargs_file)

    @type_safe
    def file__persona_digest_html(self, persona_type: Schema__Persona__Types):
        kwargs_file= dict(persona_type = persona_type,
                          file_id      = FILE_ID__PERSONA__DIGEST,
                          extension    = S3_Key__File__Extension.HTML   ,
                          content_type = S3_Key__File__Content_Type.HTML)
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

    #todo: refactor this into a method that is able to get the file contents of the file_persona.path__** files
    def persona__description__png(self, persona_type: Schema__Persona__Types):
        file_persona                   = self.file__persona(persona_type)
        path__persona__entities__png = file_persona.data().path__persona__entities__png
        kwargs = dict(s3_path        = path__persona__entities__png  ,
                      content_type   = S3_Key__File__Content_Type.TXT)
        return file_persona.hacker_news_storage.path__load_data(**kwargs)
