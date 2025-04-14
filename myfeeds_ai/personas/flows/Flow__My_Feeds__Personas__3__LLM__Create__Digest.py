from myfeeds_ai.personas.actions.My_Feeds__Persona__Data import My_Feeds__Persona__Data
from myfeeds_ai.personas.files.My_Feeds__Personas__File                                         import My_Feeds__Personas__File
from myfeeds_ai.personas.llms.LLM__Prompt__Personas__Create_Digest                              import LLM__Prompt__Personas__Create_Digest
from myfeeds_ai.personas.llms.Schema__Persona__Digest                                           import Schema__Persona__Digest
from myfeeds_ai.personas.llms.Schema__Persona__Digest_Articles                                  import Schema__Persona__Digest_Articles
from myfeeds_ai.personas.schemas.Schema__Persona                                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities                         import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                                         import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache  import Hacker_News__Execute_LLM__With_Cache
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.helpers.flows.Flow                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                  import flow
from osbot_utils.helpers.flows.decorators.task                                                  import task
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                                       import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                                      import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe


class Flow__My_Feeds__Personas__3__LLM__Create__Digest(Type_Safe):
    file_persona                         : My_Feeds__Personas__File
    persona                              : Schema__Persona
    persona_digest                       : Schema__Persona__Digest
    persona_digest_articles              : Schema__Persona__Digest_Articles
    persona_connected_entities           : Schema__Persona__LLM__Connect_Entities
    persona_type                         : Schema__Persona__Types = Schema__Persona__Types.EXEC__CISO
    #personas                             : My_Feeds__Personas
    persona_data                         : My_Feeds__Persona__Data
    prompt_create_digest                 : LLM__Prompt__Personas__Create_Digest
    output                               : dict
    path_now_file__persona_digest        : str
    path_latest_file__persona_digest     : str
    path_latest_file__persona_digest_html: str
    execute_llm_with_cache               : Hacker_News__Execute_LLM__With_Cache
    llm_request                          : Schema__LLM_Request
    llm_request__cache_id                : Obj_Id
    llm_request__cache_refresh           : bool                 = False                          # for now, force cache refresh
    llm_response                         : Schema__LLM_Response

    @task()
    def task__1__load_persona_data(self):
        with self.persona_data.file__persona(persona_type=self.persona_type) as _:
            self.file_persona = _
            self.persona      = _.data()
        with self.persona_data.file__persona_connect_entities(persona_type=self.persona_type) as _:
            self.persona_connected_entities = _.data()


    @task()
    def task__2__llm_create_persona_digest(self):
        self.llm_request = self.prompt_create_digest.llm_request(persona                    = self.persona,
                                                                 persona_connected_entities = self.persona_connected_entities)
        with self.execute_llm_with_cache.setup() as _:
            _.llm_execute.refresh_cache = self.llm_request__cache_refresh
            self.llm_response = _.execute__llm_request(self.llm_request)

        self.persona_digest_articles = self.prompt_create_digest.process_llm_response(self.llm_response)

    @task()
    def task__3__save_persona_digest(self):
        llm_request_cache          = self.execute_llm_with_cache.llm_cache
        self.llm_request__cache_id = llm_request_cache.get__cache_id__from__request(self.llm_request)


        with Schema__Persona__Digest() as _:
            _.cache_id                = self.llm_request__cache_id
            _.digest_articles         = self.persona_digest_articles
            _.digest_html             = self.persona_digest_articles.get_html(cache_id=self.llm_request__cache_id)
            _.digest_markdown         = self.persona_digest_articles.get_markdown()
            self.persona_digest       = _
        #
        with self.persona_data.file__persona_digest(persona_type=self.persona_type) as _:
            self.persona_digest.path_now = _.path_now()
            _.save_data(self.persona_digest.json())

            self.path_now_file__persona_digest    = _.path_now()
            self.path_latest_file__persona_digest = _.path_latest()

        with self.persona_data.file__persona_digest_html(persona_type=self.persona_type) as _:
            _.save_data(self.persona_digest.digest_html)
            self.path_latest_file__persona_digest_html = _.path_latest()


    @task()
    def task__4__create_output(self):
        self.output = dict(persona_type                             = self.persona_type.value                   ,
                           path_now_file__persona_digest            = self.path_now_file__persona_digest        ,
                           path_now_file__persona_digest_html       = self.path_latest_file__persona_digest_html,
                           path_now__file_llm_connected_entities    = self.path_latest_file__persona_digest     ,
                           llm_request__cache_id                    = self.llm_request__cache_id                )


    @flow()
    def create_digest(self) -> Flow:
        with self as _:
            _.task__1__load_persona_data         ()
            _.task__2__llm_create_persona_digest ()
            _.task__3__save_persona_digest       ()
            _.task__4__create_output             ()
        return self.output

    def run(self):
        return self.create_digest().execute_flow()