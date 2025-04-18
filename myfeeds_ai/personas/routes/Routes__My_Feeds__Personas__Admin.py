from osbot_fast_api.api.Fast_API_Routes                                             import Fast_API_Routes
from myfeeds_ai.personas.actions.My_Feeds__Persona                                  import My_Feeds__Persona
from myfeeds_ai.personas.actions.My_Feeds__Personas                                 import My_Feeds__Personas
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__1__Create__Persona         import Flow__My_Feeds__Personas__1__Create__Persona
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__2__LLM__Connected_Entities import Flow__My_Feeds__Personas__2__LLM__Connected_Entities
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__3__LLM__Create__Digest     import Flow__My_Feeds__Personas__3__LLM__Create__Digest
from myfeeds_ai.personas.schemas.Schema__Persona__Types                             import Schema__Persona__Types
from myfeeds_ai.pipelines.flows.Pipeline__Hacker_News__Create_Persona_Digest        import Pipeline__Hacker_News__Create_Persona_Digest
from osbot_utils.utils.Status                                                       import status_ok, status_error

ROUTE_PATH__PERSONAS = 'personas'

ROUTES_PATHS__MY_FEEDS__PERSONAS__ADMIN = [f'/{ROUTE_PATH__PERSONAS}/flow-1-create-persona'        ,
                                           f'/{ROUTE_PATH__PERSONAS}/flow-2-llm-connected-entities',
                                           f'/{ROUTE_PATH__PERSONAS}/flow-3-llm-create-digest'     ,
                                           f'/{ROUTE_PATH__PERSONAS}/files-in-latest'              ,
                                           f'/{ROUTE_PATH__PERSONAS}/files-in-now'                 ,
                                           f'/{ROUTE_PATH__PERSONAS}/storage-all-files'            ,
                                           f'/{ROUTE_PATH__PERSONAS}/delete-file'                  ]

class Routes__My_Feeds__Personas__Admin(Fast_API_Routes):
    tag          : str = ROUTE_PATH__PERSONAS
    personas     : My_Feeds__Personas

    def flow_1_create_persona(self, persona_type: Schema__Persona__Types):
        return Flow__My_Feeds__Personas__1__Create__Persona(persona_type=persona_type).run().flow_return_value

    def flow_2_llm_connected_entities(self, persona_type: Schema__Persona__Types):
        return Flow__My_Feeds__Personas__2__LLM__Connected_Entities(persona_type=persona_type).run().flow_return_value

    def flow_3_llm_create_digest(self, persona_type: Schema__Persona__Types):
        return Flow__My_Feeds__Personas__3__LLM__Create__Digest(persona_type=persona_type).run().flow_return_value

    def pipline_1_create_digest(self, persona_type: Schema__Persona__Types):
        with Pipeline__Hacker_News__Create_Persona_Digest(persona_type=persona_type) as _:
            _.create_persona_digest().execute_flow()
            return _.output

    def files_in_latest(self):
        return self.personas.files_in__latest()

    def files_in_now(self):
        return self.personas.files_in__now()

    def persona_delete(self, persona_type: Schema__Persona__Types):
        if My_Feeds__Persona(persona_type=persona_type).delete():
            return status_ok("persona deleted")
        else:
            return status_error("delete failed, because persona did not exists")

    def delete_file(self, path:str):
        return self.personas.storage.delete_from__path(path)

    def reset_description(self,  persona_type: Schema__Persona__Types):
        return My_Feeds__Persona(persona_type=persona_type).description__reset_to_default_value(force_reset=True)

    def storage_all_files(self):
        return sorted(self.personas.storage.s3_db.provider__all_files(), reverse=True)


    def setup_routes(self):
        self.add_route_get   (self.flow_1_create_persona        )
        self.add_route_get   (self.flow_2_llm_connected_entities)
        self.add_route_get   (self.flow_3_llm_create_digest     )
        self.add_route_get   (self.pipline_1_create_digest      )
        self.add_route_get   (self.files_in_latest              )
        self.add_route_get   (self.files_in_now                 )
        self.add_route_get   (self.storage_all_files            )
        self.add_route_post  (self.reset_description            )
        self.add_route_delete(self.persona_delete               )
        self.add_route_delete(self.delete_file                  )
