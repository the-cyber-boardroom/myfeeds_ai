from myfeeds_ai.personas.actions.My_Feeds__Personas         import My_Feeds__Personas
from myfeeds_ai.personas.files.My_Feeds__Personas__File     import My_Feeds__Personas__File
from myfeeds_ai.personas.schemas.Schema__Persona            import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types     import Schema__Persona__Types
from osbot_utils.helpers.flows.Flow                         import Flow
from osbot_utils.helpers.flows.decorators.flow              import flow
from osbot_utils.helpers.flows.decorators.task              import task
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.utils.Dev                                  import pprint


class Flow__My_Feeds__Personas__LLM__Connect_Entities(Type_Safe):
    file_persona              : My_Feeds__Personas__File
    file_llm_connect_entities : My_Feeds__Personas__File
    llm_connect_entities      : Schema__Persona__LLM__Connect_Entities
    persona                   : Schema__Persona
    persona_type              : Schema__Persona__Types    = Schema__Persona__Types.EXEC__CISO
    personas                  : My_Feeds__Personas
    output                    : dict

    @task()
    def task__1__load_persona_data(self):
        with self.personas.file__persona(persona_type=self.persona_type) as _:
            self.file_persona = _
            self.persona      = _.data()

    @task()
    def task__2__setup__file_llm_connect_entities(self):
        with self.personas.file__llm_connect_entities(persona_type=self.persona_type) as _:
            self.file_llm_connect_entities = _
            self.llm_connect_entities      = _.data()

        with self.llm_connect_entities as _:
            #_.persona__description__tree_values = self.persona.description__tree_values
            _.persona__path_now                 = self.persona.path_now

            # todo add LLM connection

            self.file_llm_connect_entities.save_data(_.json())
        #pprint(self.llm_connect_entities.json())



    @task()
    def task__n__create_output(self):
        self.output = dict(persona_type         = self.persona_type.value                                  ,
                           path_latest__file_llm_connect_entities = self.file_llm_connect_entities.path_latest(),
                           path_now__file_llm_connect_entities    = self.file_llm_connect_entities.path_now())


    @flow()
    def create_persona(self) -> Flow:
        with self as _:
            _.task__1__load_persona_data  ()

            #_.task__n__save_data          ()
            _.task__n__create_output      ()
        return self.output

    def run(self):
        return self.create_persona().execute_flow()