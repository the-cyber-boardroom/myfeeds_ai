from fastapi                                                                        import Response
from osbot_fast_api.api.Fast_API_Routes                                             import Fast_API_Routes
from starlette                                                                      import status
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File__Content_Type
from myfeeds_ai.personas.actions.My_Feeds__Persona                                  import My_Feeds__Persona
from myfeeds_ai.personas.actions.My_Feeds__Persona__Digest__Image                   import My_Feeds__Persona__Digest__Image
from myfeeds_ai.personas.actions.My_Feeds__Persona__Html_Page                       import My_Feeds__Persona__Html_Page
from myfeeds_ai.personas.schemas.Schema__Persona__Types                             import Schema__Persona__Types

ROUTE_PATH__PERSONAS = 'personas'

ROUTES_PATHS__MY_FEEDS__PERSONAS = [f'/{ROUTE_PATH__PERSONAS}/persona'              ,
                                    f'/{ROUTE_PATH__PERSONAS}/persona-digest'       ,
                                    f'/{ROUTE_PATH__PERSONAS}/persona-home-page'    ,
                                    f'/{ROUTE_PATH__PERSONAS}/persona-digest-image' ,
                                    f'/{ROUTE_PATH__PERSONAS}/persona-png'          ,
                                    f'/{ROUTE_PATH__PERSONAS}/persona-tree'         ]

class Routes__My_Feeds__Personas(Fast_API_Routes):
    tag          : str = ROUTE_PATH__PERSONAS

    def persona(self, persona_type: Schema__Persona__Types):
        with My_Feeds__Persona(persona_type=persona_type) as _:
            if _.exists():
                return _.data()
            else:
                return Response(status_code=status.HTTP_204_NO_CONTENT)

    def persona_digest(self, persona_type: Schema__Persona__Types):
        with My_Feeds__Persona(persona_type=persona_type) as _:
            html_code = _.persona_digest_html()
            return Response(content=html_code, media_type=str(S3_Key__File__Content_Type.HTML))

    def persona_home_page(self, persona_type: Schema__Persona__Types):
        persona = My_Feeds__Persona(persona_type=persona_type)
        with My_Feeds__Persona__Html_Page(persona=persona) as _:
            html_code = _.create()
            return Response(content=html_code, media_type=str(S3_Key__File__Content_Type.HTML))

    def persona_digest_image(self, persona_type: Schema__Persona__Types):
        persona = My_Feeds__Persona(persona_type=persona_type)
        with My_Feeds__Persona__Digest__Image(persona=persona) as _:
            title     = f'{persona_type}'
            sub_title = 'between two dates'
            png_bytes = _.generate_digest_cover(title=title, sub_title=sub_title)
            return Response(content=png_bytes, media_type=str(S3_Key__File__Content_Type.PNG))

    def persona_png(self, persona_type: Schema__Persona__Types):
        png_bytes = My_Feeds__Persona(persona_type=persona_type).persona__entities__png()
        if png_bytes:
            return Response(content=png_bytes, media_type=str(S3_Key__File__Content_Type.PNG))
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    def persona_tree(self, persona_type: Schema__Persona__Types):
        tree_values = My_Feeds__Persona(persona_type=persona_type).persona__entities__tree_values()
        if tree_values:
            return Response(content=tree_values, media_type=str(S3_Key__File__Content_Type.TXT))
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)


    def setup_routes(self):
        self.add_route_get(self.persona             )
        self.add_route_get(self.persona_digest      )
        self.add_route_get(self.persona_home_page   )
        self.add_route_get(self.persona_digest_image)
        self.add_route_get(self.persona_png         )
        self.add_route_get(self.persona_tree        )