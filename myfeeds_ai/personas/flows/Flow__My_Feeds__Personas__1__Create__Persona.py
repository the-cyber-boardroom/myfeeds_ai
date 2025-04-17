from myfeeds_ai.personas.actions.My_Feeds__Persona                  import My_Feeds__Persona
from myfeeds_ai.personas.actions.My_Feeds__Personas__Create         import My_Feeds__Personas__Create
from myfeeds_ai.personas.schemas.Schema__Persona__Types             import Schema__Persona__Types
from osbot_utils.helpers.flows.Flow                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                      import flow
from osbot_utils.helpers.flows.decorators.task                      import task
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Flow__My_Feeds__Personas__1__Create__Persona(Type_Safe):
    persona_type                       : Schema__Persona__Types    = Schema__Persona__Types.EXEC__CISO
    output                             : dict
    personas_create                    : My_Feeds__Personas__Create
    persona                            : My_Feeds__Persona              = None

    @task()
    def task__1__load_persona_data(self):
        self.persona = My_Feeds__Persona(persona_type=self.persona_type)

    @task()
    def task__2__set_persona_details(self):
        with self.persona as _:
            if _.exists() is False:                     # create persona if it doesn't exist
                _.create()

    @task()
    def task__3__create_entities(self):
        with self.persona as _:
            if not _.data().path__persona__entities:                                                            # we can use this path to determine if we need to create the entities
                persona_entities = self.personas_create.extract_entities_from_text(self.persona.description())
                self.persona.file__persona_entities().save_data(persona_entities)
                _.data().path__persona__entities = self.persona.file__persona_entities().path_now()             # update the path__persona__entities
                _.save()

    @task()
    def task__4__create_tree_values(self):
        with self.persona as _:
            if not _.data().path__persona__entities__tree_values:                                               # we can use this path to determine if we need to create the entities tree values
                file__persona_entities__tree_values = _.file__persona_entities__tree_values()
                text_entities                                 = _.persona__entities().text_entities
                tree_values                                   = self.personas_create.create_tree_values_from_entities(text_entities)
                _.data().path__persona__entities__tree_values = file__persona_entities__tree_values.path_now()
                file__persona_entities__tree_values.save_data(tree_values)
                _.save()


    @task()
    def task__5__create_description_png(self):
        with self.persona as _:
            if not _.data().path__persona__entities__png:                                                       # we can use this path to determine if we need to create the entities png
                file__persona_entities__png = _.file__persona_entities__png()
                text_entities  = _.persona__entities().text_entities
                if text_entities:
                    personas_create                       = My_Feeds__Personas__Create()
                    graph_rag                             = personas_create.prompt_extract_entities.create_entities_graph_rag(text_entities)
                    bytes_png                             = graph_rag.screenshot__create_bytes()
                    file__persona_entities__png.save_data(bytes_png)

                    with _.update() as data:
                        data.path__persona__entities__png = file__persona_entities__png.path_now()

    @task()
    def task__6__create_output(self):
        self.output = dict(persona_id          = self.persona_type         ,
                           persona             = self.persona.data().json())


    @flow()
    def create_persona(self) -> Flow:
        with self as _:
            _.task__1__load_persona_data     ()
            _.task__2__set_persona_details   ()
            _.task__3__create_entities       ()
            _.task__4__create_tree_values    ()
            _.task__5__create_description_png()
            _.task__6__create_output         ()
        return self.output

    def run(self):
        return self.create_persona().execute_flow()

