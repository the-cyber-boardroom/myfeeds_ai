from myfeeds_ai.personas.actions.My_Feeds__Personas         import My_Feeds__Personas
from myfeeds_ai.personas.files.My_Feeds__Personas__File     import My_Feeds__Personas__File
from myfeeds_ai.personas.schemas.Schema__Persona            import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Types     import Schema__Persona__Types
from osbot_utils.helpers.flows.decorators.task              import task
from osbot_utils.type_safe.Type_Safe                        import Type_Safe



class Flow__My_Feeds__Personas__3__LLM__Create__Digest(Type_Safe):
    file_persona        : My_Feeds__Personas__File
    persona             : Schema__Persona
    persona_type        : Schema__Persona__Types = Schema__Persona__Types.EXEC__CISO
    personas            : My_Feeds__Personas
    output: dict

    @task()
    def task__1__load_persona_data(self):
        with self.personas.file__persona(persona_type=self.persona_type) as _:
            self.file_persona = _
            self.persona      = _.data()
        # with self.personas.file__llm_connect_entities(persona_type=self.persona_type) as _:
        #     pprint(_.data().json())

    # @tast()
    # def task__2__load
    #     @task()
    #     def task__3__create_connected_entities(self):
    #         with self.personas.file__llm_connect_entities(persona_type=self.persona_type) as _:
    #             self.file_llm_connect_entities = _