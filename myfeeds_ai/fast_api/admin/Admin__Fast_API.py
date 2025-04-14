from osbot_fast_api.api.Fast_API                                                        import Fast_API
from myfeeds_ai.fast_api.admin.Middleware__Check_API_Key                                import Middleware__Check_API_Key
from myfeeds_ai.fast_api.admin.routes.Routes__Admin__Setup                              import Routes__Admin__Setup
from myfeeds_ai.personas.routes.Routes__My_Feeds__Personas__Admin                       import Routes__My_Feeds__Personas__Admin
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News__Flows  import Routes__Hacker_News__Flows

ENV_VAR__AUTH__MYFEEDS__API_KEY__NAME  = 'AUTH__MYFEEDS__API_KEY__NAME'
ENV_VAR__AUTH__MYFEEDS__API_KEY__VALUE = 'AUTH__MYFEEDS__API_KEY__VALUE'

ROUTES__BASE_PATH__ADMIN = '/admin'

class Admin__Fast_API(Fast_API):
    base_path = ROUTES__BASE_PATH__ADMIN

    def setup_routes(self):
        self.add_routes(Routes__Admin__Setup             )
        self.add_routes(Routes__My_Feeds__Personas__Admin)
        self.add_routes(Routes__Hacker_News__Flows       )

    # todo: replace both methods below with the version in osbot-fast-api (when that is available in pypi)

    def add_middleware__api_key_check(self):
        app = self.app()
        env_var__api_key_name  = ENV_VAR__AUTH__MYFEEDS__API_KEY__NAME
        env_var__api_key_value = ENV_VAR__AUTH__MYFEEDS__API_KEY__VALUE
        app.add_middleware(Middleware__Check_API_Key, env_var__api_key__name=env_var__api_key_name, env_var__api_key__value=env_var__api_key_value)

    def setup_middlewares(self):
        super().setup_middlewares()
        self.add_middleware__api_key_check()