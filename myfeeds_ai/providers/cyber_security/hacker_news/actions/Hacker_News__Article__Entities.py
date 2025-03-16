from mgraph_db.mgraph.actions.MGraph__Screenshot                                                        import ENV_NAME__URL__MGRAPH_DB_SERVERLESS
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                                import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News                         import FILE_ID__ARTICLE__TEXT__ENTITIES__TITLE, FILE_ID__ARTICLE__TEXT__ENTITIES__DESCRIPTION, FILE_ID__ARTICLE__TEXT__ENTITIES
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article__Text_Entities    import Hacker_News__File__Article__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.llms.prompts.LLM__Prompt__Extract_Entities         import LLM__Prompt__Extract_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Text__Entities      import Schema__Feed__Article__Text__Entities
from myfeeds_ai.utils.My_Feeds__Utils                                                                   import path_to__date_time
from osbot_utils.helpers.Obj_Id                                                                         import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe
from osbot_utils.utils.Env                                                                              import get_env
from osbot_utils.utils.Objects                                                                          import obj


class Hacker_News__Article__Entities(Type_Safe):
    article_id              : Obj_Id
    path__folder__data      : str
    prompt_extract_entities : LLM__Prompt__Extract_Entities

    def file___text__entities__mgraph(self):
        with self.file___text__entities() as _:
            _.extension     = S3_Key__File_Extension.MGRAPH__JSON
            return _

    def file___text__entities__png(self):
        with self.file___text__entities() as _:
            _.extension     = S3_Key__File_Extension.PNG
            _.content_type = "image/png"
            return _

    def file___text__entities__description(self):
        kwargs = dict(article_id = self.article_id                               ,
                      file_id    = FILE_ID__ARTICLE__TEXT__ENTITIES__DESCRIPTION ,
                      now        = self.now()                                    )
        return Hacker_News__File__Article__Text_Entities(**kwargs)

    def file___text__entities__description__mgraph(self):
        with self.file___text__entities__description() as _:
            _.extension     = S3_Key__File_Extension.MGRAPH__JSON
            return _

    def file___text__entities(self):
        kwargs = dict(article_id = self.article_id                         ,
                      file_id    = FILE_ID__ARTICLE__TEXT__ENTITIES        ,
                      now        = self.now()                              )
        return Hacker_News__File__Article__Text_Entities(**kwargs)

    def file___text__entities__title(self):
        kwargs = dict(article_id = self.article_id                         ,
                      file_id    = FILE_ID__ARTICLE__TEXT__ENTITIES__TITLE ,
                      now        = self.now()                              )
        return Hacker_News__File__Article__Text_Entities(**kwargs)

    def file___text__entities__title__mgraph(self):
        with self.file___text__entities__title() as _:
            _.extension     = S3_Key__File_Extension.MGRAPH__JSON
            return _

    def file___text__entities__title__png(self):
        with self.file___text__entities__title() as _:
            _.extension     = S3_Key__File_Extension.PNG
            _.content_type = "image/png"
            return _

    def file___text__entities__description__png(self):
        with self.file___text__entities__description() as _:
            _.extension     = S3_Key__File_Extension.PNG
            _.content_type = "image/png"
            return _

    def create__text_entities__mgraph_and_png(self, file_with_entities: Hacker_News__File__Article__Text_Entities):
        json_data              = file_with_entities.load()
        text_entities          = Schema__Feed__Article__Text__Entities.from_json(json_data).text_entities
        text_entities.entities = text_entities.entities
        graph_rag              = self.prompt_extract_entities.create_entities_graph_rag(entities=text_entities)   # Create the MGraph with the text_entities
        mgraph_entity          = graph_rag.mgraph_entity
        if get_env(ENV_NAME__URL__MGRAPH_DB_SERVERLESS):                                                          # is this env var is not set we can't create the graph's png
            try:
                png_bytes = graph_rag.screenshot__create_bytes()                                                  # create the bytes (using the lambda graphviz lambda function)
            except Exception as e:
                print(e)                                                                                          # todo: add better error handling and reporting
                png_bytes = None
        else:
            png_bytes = None
        return dict(mgraph_entity=mgraph_entity, png_bytes=png_bytes)

    def create_text_entities_graph__description(self):
        kwargs = dict(file___text__entities         = self.file___text__entities__description()        ,
                      file___text__entities__mgraph = self.file___text__entities__description__mgraph(),
                      file___text__entities__png    = self.file___text__entities__description__png   ())
        return self.create_text_entities_graph__files(**kwargs)

    def create_text_entities_graph__title(self):
        kwargs = dict(file___text__entities         = self.file___text__entities__title()         ,
                      file___text__entities__mgraph = self.file___text__entities__title__mgraph() ,
                      file___text__entities__png    = self.file___text__entities__title__png   ())
        return self.create_text_entities_graph__files(**kwargs)

    def create_text_entities_graph__files(self, file___text__entities, file___text__entities__mgraph, file___text__entities__png):
        path__file__text_entities__mgraph = None
        path__file__text_entities__png    = None

        if file___text__entities__png.exists() is False or file___text__entities__mgraph.exists() is False:
            result        = self.create__text_entities__mgraph_and_png(file___text__entities)
            mgraph_entity = result.get('mgraph_entity')
            png_bytes     = result.get('png_bytes'    )
            if mgraph_entity:
                path__file__text_entities__mgraph = file___text__entities__mgraph.save_data(mgraph_entity.json())
            if png_bytes:
                path__file__text_entities__png    = file___text__entities__png   .save_data(png_bytes           )
        else:
            path__file__text_entities__mgraph  = file___text__entities__mgraph.path_now()
            if file___text__entities__png.exists():
                path__file__text_entities__png = file___text__entities__png.path_now()

        return obj(dict(path__file__text_entities__mgraph = path__file__text_entities__mgraph,
                        path__file__text_entities__png    = path__file__text_entities__png   ))


    def now(self):
        if self.path__folder__data:
            return path_to__date_time(self.path__folder__data)