from fastapi                                                                import Response
from osbot_fast_api.api.Fast_API_Routes                                     import Fast_API_Routes
from starlette                                                              import status
from myfeeds_ai.personas.actions.My_Feeds__Personas                         import My_Feeds__Personas
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__Create__Persona    import Flow__My_Feeds__Personas__Create__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Types                     import Schema__Persona__Types

ROUTE_PATH__PERSONAS = 'personas'

ROUTES_PATHS__MY_FEEDS__PERSONAS = [f'/{ROUTE_PATH__PERSONAS}/files-in-latest'    ,
                                    f'/{ROUTE_PATH__PERSONAS}/files-in-now'       ,
                                    f'/{ROUTE_PATH__PERSONAS}/flow-create-persona',
                                    f'/{ROUTE_PATH__PERSONAS}/persona',
                                    f'/{ROUTE_PATH__PERSONAS}/persona-png',
                                    f'/{ROUTE_PATH__PERSONAS}/persona-tree']

class Routes__My_Feeds__Personas(Fast_API_Routes):
    tag: str = ROUTE_PATH__PERSONAS
    personas : My_Feeds__Personas

    def flow_create_persona(self, persona_type: Schema__Persona__Types):
        return Flow__My_Feeds__Personas__Create__Persona(persona_type=persona_type).run().flow_return_value

    def files_in_latest(self):
        return self.personas.files_in__latest()

    def files_in_now(self):
        return self.personas.files_in__now()

    def persona(self, persona_type: Schema__Persona__Types):
        return self.personas.file__persona(persona_type=persona_type).load()

    def persona_png(self, persona_type: Schema__Persona__Types):
        png_bytes = self.personas.persona__description__png(persona_type=persona_type)
        if png_bytes:
            content_type = "image/png"
            return Response(content=png_bytes, media_type=content_type)
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    def persona_tree(self, persona_type: Schema__Persona__Types):
        tree_values = self.personas.persona__description__tree_values(persona_type=persona_type)
        if tree_values:
            content_type = 'text/plain; charset=utf-8'
            return Response(content=tree_values, media_type=content_type)
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    def setup_routes(self):
        self.add_route_get(self.flow_create_persona)
        self.add_route_get(self.files_in_latest    )
        self.add_route_get(self.files_in_now       )
        self.add_route_get(self.persona            )
        self.add_route_get(self.persona_png        )
        self.add_route_get(self.persona_tree       )
