from myfeeds_ai.personas.actions.My_Feeds__Personas import My_Feeds__Personas
from myfeeds_ai.personas.files.My_Feeds__Personas__File import My_Feeds__Personas__File
from myfeeds_ai.personas.llms.LLM__Prompt__Personas__Extract_Entities import LLM__Prompt__Personas__Extract_Entities
from osbot_utils.helpers.Safe_Id                    import Safe_Id
from osbot_utils.helpers.flows.Flow                 import Flow
from osbot_utils.helpers.flows.decorators.flow      import flow
from osbot_utils.helpers.flows.decorators.task      import task
from osbot_utils.type_safe.Type_Safe                import Type_Safe


class Flow__My_Feeds__Personas__Create__Persona(Type_Safe):
    persona_name            : Safe_Id
    output                  : dict
    prompt_extract_entities : LLM__Prompt__Personas__Extract_Entities
    personas                : My_Feeds__Personas
    file_persona            : My_Feeds__Personas__File

    @task()
    def task__1__load_persona_data(self):
        with self.personas.file__persona__ciso() as _:
            self.file_persona = _
            self.persona_name = _.file_id


    @task()
    def task__n__create_output(self):
        self.output = dict(persona_name = self.persona_name              ,
                           path_now     = self.file_persona.path_now()   ,
                           path_latest  = self.file_persona.path_latest())


    @flow()
    def create_persona(self) -> Flow:
        with self as _:
            _.task__1__load_persona_data ()
            _.task__n__create_output     ()
        return self.output

    def run(self):
        return self.create_persona().execute_flow()

