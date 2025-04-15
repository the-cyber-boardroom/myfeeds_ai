from typing import Dict

from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File__Content_Type
from myfeeds_ai.personas.actions.My_Feeds__Persona                                              import My_Feeds__Persona
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now                                    import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.llms.LLM__Prompt__Connect_Entities                                     import LLM__Prompt__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                                         import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Feed__Text_Entities   import Hacker_News__Feed__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage               import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File                    import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache  import Hacker_News__Execute_LLM__With_Cache
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Text_Entities__Files import Schema__Feed__Text_Entities__Files
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.helpers.flows.Flow                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                  import flow
from osbot_utils.helpers.flows.decorators.task                                                  import task
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Dev import pprint


class Flow__My_Feeds__Personas__2__LLM__Connected_Entities(Type_Safe):
    persona_type                                : Schema__Persona__Types    = Schema__Persona__Types.EXEC__CISO
    persona                                     : My_Feeds__Persona
    hacker_news_storage                         : Hacker_News__Storage              # required to get the content of the markdown files

    feed_text_entities__files                   : Schema__Feed__Text_Entities__Files
    feed_text_entities                          : Hacker_News__Feed__Text_Entities
    file__feed_text_entities__files             : Hacker_News__File
    file__persona_articles__connected_entities  : My_Feeds__Personas__File__Now

    output                                      : dict

    #path_now__persona__tree_values              : str                             = None
    path_now__entities__titles__tree_values     : str                             = None

    articles_graph_tree                         : str                             = None
    persona_graph_tree                          : str                             = None
    articles_markdown                           : Dict[Obj_Id, str]



    @task()
    def task__1__load_persona_data(self):
        self.persona                         = My_Feeds__Persona(persona_type=self.persona_type)
        self.persona_graph_tree              = self.persona.persona__entities__tree_values()
        #self.path_now__persona__tree_values = self.persona.file__persona_entities__tree_values().path_now()
        # with self.persona_data as _:
        #     self.file__persona                       = _.file__persona                      (persona_type=self.persona_type)
        #     self.file__persona_entities              = _.file__persona_entities             (persona_type=self.persona_type)
        #     self.file__persona_connect_entities      = _.file__persona_connect_entities     (persona_type=self.persona_type)
        #     self.file__persona_entities__tree_values = _.file__persona_entities__tree_values(persona_type=self.persona_type)
        #
        # self.file__feed_text_entities__files  = self.feed_text_entities.file__feed_text_entities__files()
        #
        # self.persona                       = self.file__persona.data                      ()
        # self.persona_entities              = self.file__persona_entities.data             ()
        # #self.persona_entities__tree_values = self.file__persona_entities__tree_values.data()
        # pprint(self.file__persona_entities__tree_values.data())

        # todo: is file__persona_connect_entities the same as file__llm_connect_entities ?
        #self.llm_connect_entities = self.file__llm_connect_entities.data()     # todo see if I need this

    @task()
    def task__2__load_articles_data(self):
        self.articles_graph_tree                     = self.feed_text_entities.tree_view__entities__titles()
        self.path_now__entities__titles__tree_values = self.feed_text_entities.text_entities__files().path_now__text_entities__titles__tree
        #pprint( self.feed_text_entities.file__feed_text_entities__files().data().json())
        return
        #self.feed_text_entities__files             = self.file__feed_text_entities__files.data()
        #self.path_now__text_entities__titles__tree = self.feed_text_entities__files.path_now__text_entities__titles__tree
        #self.articles_graph_tree                   = self.hacker_news_storage.path__load_data(self.path_now__text_entities__titles__tree, content_type=S3_Key__File__Content_Type.TXT).decode()
        #self.persona_graph_tree                    = self.persona.persona__entities__tree_values()

        # return
        # with self.feed_text_entities.file__feed_text_entities__files().data() as _:
        #
        #     self.path_now__text_entities__titles__tree = _.path_now__text_entities__titles__tree
        #     if self.path_now__text_entities__titles__tree:
        #         self.articles_graph_tree = self.hacker_news_storage.path__load_data(self.path_now__text_entities__titles__tree, content_type=S3_Key__File__Content_Type.TXT).decode()
        #         self.persona_graph_tree  = self.persona.description__tree_values
        #     else:
        #         raise ValueError(f"path_now__text_entities__titles__tree was empty in file: {self.feed_text_entities.file__feed_text_entities__files().path_now()} ")
        #
        #     #path_latest__text_entities__titles__tree

    @task()
    def task__3__create_connected_entities(self):
        # with self.persona_data.file__persona_connect_entities(persona_type=self.persona_type) as _:
        #     self.file_llm_connect_entities = _
        #     self.llm_connect_entities      = _.data()

        prompt_connect_entities = LLM__Prompt__Connect_Entities()

        llm_request             = prompt_connect_entities.llm_request(persona_graph_tree  = self.persona_graph_tree ,
                                                                      articles_graph_tree = self.articles_graph_tree)
        with Hacker_News__Execute_LLM__With_Cache() as _:
            llm_response                = _.setup().execute__llm_request(llm_request)
            persona_connected_entities  = prompt_connect_entities.process_llm_response(llm_response)
            cache_id__llm_request       = _.llm_cache.get__cache_id__from__request(llm_request)

        # assign save data into file__persona_articles__connected_entities
        with  self.persona.file__persona_articles__connected_entities().update() as _:
            _.path__now__persona                       = self.persona.data().path__now
            _.path__now__persona__tree_values          = self.persona.data().path__persona__entities__tree_values
            _.path__now__entities__titles__tree_values = self.path_now__entities__titles__tree_values
            _.connected_entities                      = persona_connected_entities.connected_entities
            _.cache_id__llm_request                   = cache_id__llm_request

        # update the main persona file with the path to the file created above
        with self.persona.file__persona().update() as _:
            _.path__persona__articles__connected_entities = self.persona.file__persona_articles__connected_entities().data().path__now

    @task()
    def task__4__collect_articles_markdown(self):
        file_current_articles = Hacker_News__File__Articles__Current()
        file_current_articles.load()
        with  self.persona.file__persona_articles__connected_entities().update() as _:
        #with self.persona_data.file__persona_connect_entities(persona_type=self.persona_type) as _:
            #llm_connect_entities = _.data()
            for connected_entity in _.connected_entities:
                article_id = Obj_Id(connected_entity.article_id)
                article    = file_current_articles.article(article_id=article_id)
                if article:
                    path__file__markdown = article.path__file__markdown
                    markdown_content = self.hacker_news_storage.path__load_data(path__file__markdown, content_type=S3_Key__File__Content_Type.TXT).decode()
                    #print(markdown_content)
                    _.articles_markdown[article_id] = markdown_content

            # _.save_data(llm_connect_entities.json())
            # self.articles_markdown  = llm_connect_entities.articles_markdown
                    # from osbot_utils.utils.Dev import pprint
                    # pprint(article.json())


    @task()
    def task__5__create_output(self):
        self.output = dict(persona_type                             = self.persona_type.value                         ,
                           persona                                  = self.persona.file__persona().load()               ,
                           #path_latest__file_llm_connected_entities = self.file_llm_connect_entities.path_latest    (),
                           #path_now__file_llm_connected_entities    = self.file_llm_connect_entities.path_now       (),
                           size__articles_graph_tree                = len(self.articles_graph_tree                   ),
                           size__persona_graph_tree                 = len(self.persona_graph_tree                    ),
                           size_articles_markdown                   = len(self.articles_markdown)                     )
                           #llm_request_cache_id                     = self.llm_connect_entities.cache_id__llm_request )



    @flow()
    def create_persona(self) -> Flow:
        with self as _:
            _.task__1__load_persona_data         ()
            _.task__2__load_articles_data        ()
            _.task__3__create_connected_entities ()
            _.task__4__collect_articles_markdown ()
            _.task__5__create_output             ()
        return self.output

    def run(self):
        return self.create_persona().execute_flow()