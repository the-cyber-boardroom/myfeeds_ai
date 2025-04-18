from typing import Dict

from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File__Content_Type
from myfeeds_ai.personas.actions.My_Feeds__Persona                                              import My_Feeds__Persona
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now                                    import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.llms.LLM__Prompt__Connect_Entities                                     import LLM__Prompt__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Articles__Connected_Entities                  import Schema__Persona__Articles__Connected_Entities
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

class Flow__My_Feeds__Personas__2__LLM__Connected_Entities(Type_Safe):
    persona_type                                : Schema__Persona__Types    = Schema__Persona__Types.EXEC__CISO
    persona                                     : My_Feeds__Persona
    hacker_news_storage                         : Hacker_News__Storage              # required to get the content of the markdown files

    feed_text_entities                          : Hacker_News__Feed__Text_Entities
    file__feed_text_entities__files             : Hacker_News__File
    file__persona_articles__connected_entities  : My_Feeds__Personas__File__Now
    persona__articles__connected_entities       : Schema__Persona__Articles__Connected_Entities
    paths__feed__text_entities                  : Schema__Feed__Text_Entities__Files
    text_entities_changed                       : bool
    output                                      : dict

    #path_now__persona__tree_values              : str                             = None
    path_now__entities__titles__tree_values     : str                             = None

    articles_graph_tree                         : str
    persona_graph_tree                          : str
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
        self.paths__feed__text_entities = self.feed_text_entities.text_entities__files()
        self.persona__articles__connected_entities = self.persona.persona__articles__connected_entities()
        with self.persona__articles__connected_entities as _:
            if _.paths__feed__text_entities is None:                                                # check if this is the first time we are doing this
                self.text_entities_changed = True
            elif _.paths__feed__text_entities.json() != self.paths__feed__text_entities.json():     # of if the contents has changed (i.e. one of the paths, which is updated when the text entities are recreated)
                self.text_entities_changed = True

        #self.text_entities_changed = True

        if self.text_entities_changed:
            self.articles_graph_tree                     = self.feed_text_entities.tree_view__entities__titles()
            self.path_now__entities__titles__tree_values = self.feed_text_entities.text_entities__files().path_now__text_entities__titles__tree


    @task()
    def task__3__create_connected_entities(self):
        if self.text_entities_changed:
            prompt_connect_entities = LLM__Prompt__Connect_Entities()
            llm_request             = prompt_connect_entities.llm_request(persona_graph_tree  = self.persona_graph_tree ,
                                                                          articles_graph_tree = self.articles_graph_tree)
            with Hacker_News__Execute_LLM__With_Cache().setup() as _:
                llm_response                = _.execute__llm_request(llm_request)
                persona_connected_entities  = prompt_connect_entities.process_llm_response(llm_response)
                cache_id__llm_request       = _.llm_cache.get__cache_id__from__request(llm_request)

            # assign save data into file__persona_articles__connected_entities
            with  self.persona.file__persona_articles__connected_entities().update() as _:
                _.path__now__persona                       = self.persona.data().path__now
                _.path__now__entities__titles__tree_values = self.path_now__entities__titles__tree_values
                _.paths__feed__text_entities               = self.paths__feed__text_entities.json()
                _.connected_entities                       = persona_connected_entities.connected_entities
                _.cache_id__llm_request                    = cache_id__llm_request

            # update the main persona file with the path to the file created above
            with self.persona.file__persona().update() as _:
                _.path__persona__articles__connected_entities = self.persona.file__persona_articles__connected_entities().data().path__now  # update to latest value
                _.path__persona__digest                       = ''                                                                          # clear these values since the digest html is out of date now
                _.path__persona__digest__html                 = ''


    #@task()
    def task__4__collect_articles_markdown(self):
        if self.text_entities_changed:
            file_current_articles = Hacker_News__File__Articles__Current()
            file_current_articles.load()
            persona__articles__connected_entities = self.persona.persona__articles__connected_entities()
            connected_entities                    = persona__articles__connected_entities.connected_entities
            articles_markdown                     = {}
            for connected_entity in connected_entities:
                article_id = Obj_Id(connected_entity.article_id)
                article    = file_current_articles.article(article_id=article_id)
                if article:
                    path__file__markdown = article.path__file__markdown
                    markdown_content = self.hacker_news_storage.path__load_data(path__file__markdown, content_type=S3_Key__File__Content_Type.TXT).decode()
                    articles_markdown[article_id] = markdown_content

            persona__articles__connected_entities.articles_markdown = articles_markdown

            self.persona.file__persona_articles__connected_entities().save_data(persona__articles__connected_entities)
                # _.save_data(llm_connect_entities.json())
                # self.articles_markdown  = llm_connect_entities.articles_markdown
                        # from osbot_utils.utils.Dev import pprint
                        # pprint(article.json())


    @task()
    def task__5__create_output(self):
        self.output = dict(persona_type                             = self.persona_type.value               ,
                           persona                                  = self.persona.file__persona().load()   ,
                           size__articles_graph_tree                = len(self.articles_graph_tree         ),
                           size__persona_graph_tree                 = len(self.persona_graph_tree          ),
                           size_articles_markdown                   = len(self.articles_markdown           ),
                           text_entities_changed                    = self.text_entities_changed            ,
                           paths__feed__text_entities               = self.paths__feed__text_entities.json())



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