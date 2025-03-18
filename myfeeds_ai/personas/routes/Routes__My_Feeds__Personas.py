from osbot_fast_api.api.Fast_API_Routes                                     import Fast_API_Routes
from myfeeds_ai.personas.actions.My_Feeds__Personas                         import My_Feeds__Personas
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__Create__Persona    import Flow__My_Feeds__Personas__Create__Persona

ROUTE_PATH__PERSONAS = 'personas'

ROUTES_PATHS__MY_FEEDS__PERSONAS = [f'/{ROUTE_PATH__PERSONAS}/files-in-latest'    ,
                                    f'/{ROUTE_PATH__PERSONAS}/files-in-now'       ,
                                    f'/{ROUTE_PATH__PERSONAS}/persona-ciso'       ,
                                    f'/{ROUTE_PATH__PERSONAS}/flow-create-persona']

class Routes__My_Feeds__Personas(Fast_API_Routes):
    tag: str = ROUTE_PATH__PERSONAS
    personas : My_Feeds__Personas

    def flow_create_persona(self):
        return Flow__My_Feeds__Personas__Create__Persona().run().flow_return_value

    def files_in_latest(self):
        return self.personas.files_in__latest()

    def files_in_now(self):
        return self.personas.files_in__now()

    def persona_ciso(self):
        return self.personas.persona__ciso()

    def setup_routes(self):
        self.add_route_get(self.flow_create_persona)
        self.add_route_get(self.files_in_latest    )
        self.add_route_get(self.files_in_now       )
        self.add_route_get(self.persona_ciso       )