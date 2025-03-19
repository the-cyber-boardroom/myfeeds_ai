from myfeeds_ai.personas.actions.My_Feeds__Personas                import My_Feeds__Personas
from myfeeds_ai.personas.actions.My_Feeds__Personas__Create        import My_Feeds__Personas__Create
from myfeeds_ai.personas.files.My_Feeds__Personas__File            import My_Feeds__Personas__File
from myfeeds_ai.personas.schemas.Default_Data__My_Feeds__Personas  import Default_Data__My_Feeds__Personas
from myfeeds_ai.personas.schemas.Schema__Persona                   import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Types            import Schema__Persona__Types
from osbot_utils.helpers.Safe_Id                                   import Safe_Id
from osbot_utils.helpers.flows.Flow                                import Flow
from osbot_utils.helpers.flows.decorators.flow                     import flow
from osbot_utils.helpers.flows.decorators.task                     import task
from osbot_utils.type_safe.Type_Safe                               import Type_Safe
from osbot_utils.utils.Dev                                         import pprint


class Flow__My_Feeds__Personas__1__Create__Persona(Type_Safe):
    persona_type            : Schema__Persona__Types    = Schema__Persona__Types.EXEC__CISO
    output                  : dict
    personas_create         : My_Feeds__Personas__Create
    personas                : My_Feeds__Personas
    file_persona            : My_Feeds__Personas__File
    persona                 : Schema__Persona

    @task()
    def task__1__load_persona_data(self):
        with self.personas.file__persona(persona_type=self.persona_type) as _:
            self.file_persona = _
            self.persona      = _.data()

    @task()
    def test__2__set_persona_details(self):
        with self.persona as _:
            if _.description is None:
                persona_default_data = Default_Data__My_Feeds__Personas.get(self.persona_type)
                if persona_default_data:
                    _.description  = persona_default_data.get("description")
            _.persona_type = self.persona_type

    @task()
    def test__3__create_entities(self):
        with self.persona as _:
            text = _.description
            persona_text_entities                        = self.personas_create.extract_entities_from_text(text)
            _.description__entities                      = persona_text_entities.text_entities
            _.cache_ids[Safe_Id('description-entities')] = persona_text_entities.cache_id

    #@task()
    def task__4__create_tree_values(self):
        with self.persona as _:
            text_entities              =  _.description__entities
            tree_values                = self.personas_create.create_tree_values_from_entities(text_entities)
            _.description__tree_values = tree_values

            #print(_.description__tree_values)

    @task()
    def task__5__save_data(self):
        with self.persona as _:
            _.path_now    = self.file_persona.path_now()
            _.path_latest = self.file_persona.path_latest()
        with self.file_persona as _:
            pprint(_.save_data(self.persona.json()))

    @task()
    def task__6__create_output(self):
        self.output = dict(persona_id   = self.persona_type,
                           path_now     = self.file_persona.path_now(),
                           path_latest  = self.file_persona.path_latest(),
                           persona      = self.persona.json())


    @flow()
    def create_persona(self) -> Flow:
        with self as _:
            _.task__1__load_persona_data  ()
            _.test__2__set_persona_details()
            _.test__3__create_entities    ()
            _.task__4__create_tree_values ()
            _.task__5__save_data          ()
            _.task__6__create_output      ()
        return self.output

    def run(self):
        return self.create_persona().execute_flow()

