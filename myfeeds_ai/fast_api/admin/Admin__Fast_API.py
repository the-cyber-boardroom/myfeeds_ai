from osbot_fast_api.api.Fast_API                                                        import Fast_API
from myfeeds_ai.fast_api.admin.routes.Routes__Admin__Setup                              import Routes__Admin__Setup
from myfeeds_ai.fast_api.admin.routes.Routes__Debug                                     import Routes__Debug
from myfeeds_ai.personas.routes.Routes__My_Feeds__Personas__Admin                       import Routes__My_Feeds__Personas__Admin
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News__Flows  import Routes__Hacker_News__Flows

ROUTES__BASE_PATH__ADMIN = '/admin'

class Admin__Fast_API(Fast_API):
    base_path      : str  = ROUTES__BASE_PATH__ADMIN
    enable_api_key : bool = True

    def setup_routes(self):
        self.add_routes(Routes__Admin__Setup             )
        self.add_routes(Routes__My_Feeds__Personas__Admin)
        self.add_routes(Routes__Hacker_News__Flows       )
        self.add_routes(Routes__Debug                    )