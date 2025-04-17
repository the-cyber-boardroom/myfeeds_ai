from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__1__Create__Persona                 import Flow__My_Feeds__Personas__1__Create__Persona
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__2__LLM__Connected_Entities         import Flow__My_Feeds__Personas__2__LLM__Connected_Entities
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__3__LLM__Create__Digest             import Flow__My_Feeds__Personas__3__LLM__Create__Digest
from myfeeds_ai.personas.schemas.Schema__Persona__Types                                     import Schema__Persona__Types
from osbot_utils.helpers.flows.Flow                                                         import Flow
from osbot_utils.helpers.flows.decorators.flow                                              import flow
from osbot_utils.helpers.flows.decorators.task                                              import task
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe


class Pipeline__Hacker_News__Create_Persona_Digest(Type_Safe):
    persona_type                       : Schema__Persona__Types = Schema__Persona__Types.EXEC__CISO
    output                             : dict
    output__flow_1__create_persona     : dict
    output__flow_2__connected_entities : dict
    output__flow_3__create_digest      : dict
    flow_1__create_persona             : Flow__My_Feeds__Personas__1__Create__Persona
    flow_2__connected_entities         : Flow__My_Feeds__Personas__2__LLM__Connected_Entities
    flow_3__create_digest              : Flow__My_Feeds__Personas__3__LLM__Create__Digest
    flow_1__execute                    : bool  = True
    flow_2__execute                    : bool  = True
    flow_3__execute                    : bool  = True

    @task()
    def task__1__execute_flow_1__create_persona(self):
        if self.flow_1__execute:
            self.flow_1__create_persona         = Flow__My_Feeds__Personas__1__Create__Persona(persona_type=self.persona_type)
            self.output__flow_1__create_persona = self.flow_1__create_persona.run().flow_return_value

    @task()
    def task__2__execute_flow_2__connected_entities(self):
        if self.flow_2__execute:
            self.flow_2__connected_entities         = Flow__My_Feeds__Personas__2__LLM__Connected_Entities(persona_type=self.persona_type)
            self.output__flow_2__connected_entities = self.flow_2__connected_entities.run().flow_return_value

    @task()
    def task__3__execute_flow_3__create_digest(self):
        if self.flow_3__execute:
            self.flow_3__create_digest         = Flow__My_Feeds__Personas__3__LLM__Create__Digest(persona_type=self.persona_type)
            self.output__flow_3__create_digest = self.flow_3__create_digest.run().flow_return_value

    @task()
    def task__n__create_output(self):
        self.output = dict(output__flow_1__create_persona     = self.output__flow_1__create_persona     ,
                           output__flow_2__connected_entities = self.output__flow_2__connected_entities ,
                           output__flow_3__create_digest      = self.output__flow_3__create_digest      )


    @flow()
    def create_persona_digest(self) -> Flow:
        with self as _:
            _.task__1__execute_flow_1__create_persona    ()
            _.task__2__execute_flow_2__connected_entities()
            _.task__3__execute_flow_3__create_digest     ()
            _.task__n__create_output                     ()
        #return self.output

    def run(self):
        return self.create_persona_digest().execute_flow()