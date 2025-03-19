from typing import Dict

from myfeeds_ai.personas.actions.My_Feeds__Personas                                             import My_Feeds__Personas
from myfeeds_ai.personas.files.My_Feeds__Personas__File                                         import My_Feeds__Personas__File
from myfeeds_ai.personas.llms.LLM__Prompt__Connect_Entities                                     import LLM__Prompt__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona                                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities                         import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                                         import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Feed__Text_Entities   import Hacker_News__Feed__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage               import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache  import Hacker_News__Execute_LLM__With_Cache
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.helpers.flows.Flow                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                  import flow
from osbot_utils.helpers.flows.decorators.task                                                  import task
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe


class Flow__My_Feeds__Personas__2__LLM__Connected_Entities(Type_Safe):
    file_persona                          : My_Feeds__Personas__File
    file_llm_connect_entities             : My_Feeds__Personas__File
    feed_text_entities                    : Hacker_News__Feed__Text_Entities
    hacker_news_storage                   : Hacker_News__Storage
    llm_connect_entities                  : Schema__Persona__LLM__Connect_Entities
    persona                               : Schema__Persona
    persona_type                          : Schema__Persona__Types    = Schema__Persona__Types.EXEC__CISO
    personas                              : My_Feeds__Personas
    output                                : dict
    path_now__text_entities__titles__tree : str
    articles_graph_tree                   : str
    persona_graph_tree                    : str
    articles_markdown                     : Dict[Obj_Id, str]

    @task()
    def task__1__load_persona_data(self):
        with self.personas.file__persona(persona_type=self.persona_type) as _:
            self.file_persona = _
            self.persona      = _.data()


    @task()
    def task__2__load_articles_data(self):
        with self.feed_text_entities.file__feed_text_entities__files().data() as _:

            self.path_now__text_entities__titles__tree = _.path_now__text_entities__titles__tree

            self.articles_graph_tree = self.hacker_news_storage.path__load_data(self.path_now__text_entities__titles__tree, content_type='text/plain').decode()
            self.persona_graph_tree  = self.persona.description__tree_values

            #path_latest__text_entities__titles__tree

    #@task()
    def task__3__create_connected_entities(self):
        with self.personas.file__llm_connect_entities(persona_type=self.persona_type) as _:
            self.file_llm_connect_entities = _
            self.llm_connect_entities      = _.data()

        prompt_connect_entities = LLM__Prompt__Connect_Entities()

        llm_request             = prompt_connect_entities.llm_request(persona_graph_tree  = self.persona_graph_tree ,
                                                                      articles_graph_tree = self.articles_graph_tree)
        with Hacker_News__Execute_LLM__With_Cache() as _:
            llm_response                = _.setup().execute__llm_request(llm_request)
            persona_connected_entities  = prompt_connect_entities.process_llm_response(llm_response)
            cache_id__llm_request       = _.llm_cache.get__cache_id__from__request(llm_request)

        with self.llm_connect_entities as _:
            _.persona__path_now                     = self.persona.path_now
            _.path_now__text_entities__titles__tree = self.path_now__text_entities__titles__tree
            _.connected_entities                    = persona_connected_entities.connected_entities
            _.cache_id__llm_request                 = cache_id__llm_request
            self.file_llm_connect_entities.save_data(_.json())

    @task()
    def task__4__collect_articles_markdown(self):
        file_current_articles = Hacker_News__File__Articles__Current()
        file_current_articles.load()
        with self.personas.file__llm_connect_entities(persona_type=self.persona_type) as _:
            llm_connect_entities = _.data()
            for connected_entity in llm_connect_entities.connected_entities:
                article_id = Obj_Id(connected_entity.article_id)
                article    = file_current_articles.article(article_id=article_id)
                if article:
                    path__file__markdown = article.path__file__markdown
                    markdown_content = self.hacker_news_storage.path__load_data(path__file__markdown, content_type='text/plain').decode()
                    #print(markdown_content)
                    llm_connect_entities.articles_markdown[article_id] = markdown_content

            _.save_data(llm_connect_entities.json())
            self.articles_markdown  = llm_connect_entities.articles_markdown
                    # from osbot_utils.utils.Dev import pprint
                    # pprint(article.json())


    @task()
    def task__n__create_output(self):
        self.output = dict(persona_type                             = self.persona_type.value                         ,
                           path_latest__file_llm_connected_entities = self.file_llm_connect_entities.path_latest    (),
                           path_now__file_llm_connected_entities    = self.file_llm_connect_entities.path_now       (),
                           size__articles_graph_tree                = len(self.articles_graph_tree                   ),
                           size__persona_graph_tree                 = len(self.persona_graph_tree                    ),
                           size_articles_markdown                   = len(self.articles_markdown)                     ,
                           llm_request_cache_id                     = self.llm_connect_entities.cache_id__llm_request )



    @flow()
    def create_persona(self) -> Flow:
        with self as _:
            _.task__1__load_persona_data         ()
            _.task__2__load_articles_data        ()
            _.task__3__create_connected_entities ()
            _.task__4__collect_articles_markdown ()
            _.task__n__create_output             ()
        return self.output

    def run(self):
        return self.create_persona().execute_flow()