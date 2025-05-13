import myfeeds_ai
from starlette.staticfiles                                                                  import StaticFiles
from myfeeds_ai.fast_api.admin.Admin__Fast_API                                              import Admin__Fast_API
from myfeeds_ai.fast_api.public_data.LLM_Cache__Fast_API                                    import LLM_Cache__Fast_API
from myfeeds_ai.fast_api.public_data.Public_Data__Fast_API                                  import Public_Data__Fast_API
from myfeeds_ai.personas.routes.Routes__My_Feeds__Personas                                  import Routes__My_Feeds__Personas
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.routes.Routes__Docs_DinisCruz_Ai import Routes__Docs_DinisCruz_Ai
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News__Articles   import Routes__Hacker_News__Articles
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News__Cache      import Routes__Hacker_News__Cache
from myfeeds_ai.providers.cyber_security.owasp.routes.Routes__Owasp                         import Routes__Owasp
from myfeeds_ai.rss_feeds.RSS_Feeds__Fast_API                                               import RSS_Feeds__Fast_API
from osbot_utils.utils.Env                                                                  import get_env, load_dotenv
from osbot_fast_api.api.Fast_API                                                            import Fast_API
from myfeeds_ai                                                                             import web_ui
from osbot_utils.utils.Files                                                                import path_combine
from myfeeds_ai.fast_api.routes.Routes__Info                                                import Routes__Info
from myfeeds_ai.providers.cyber_security.open_security_summit.routes.Routes__OSS            import Routes__OSS
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News             import Routes__Hacker_News


# todo: refactor Data_Feeds class name
class Data_Feeds__Fast_API(Fast_API):
    base_path  : str  = '/'
    enable_cors: bool = True

    def add_static_ui(self):
        path_static_folder = web_ui.path
        path_name   = "ui"
        path_static = f"/{path_name}"
        self.app().mount(path_static, StaticFiles(directory=path_static_folder), name=path_name)

    def setup_routes(self):
        self.add_routes(Routes__Info                 )
        self.add_routes(Routes__My_Feeds__Personas   )
        self.add_routes(Routes__Hacker_News__Articles)
        self.add_routes(Routes__Hacker_News          )
        self.add_routes(Routes__Docs_DinisCruz_Ai    )
        self.add_routes(Routes__Owasp                )
        self.add_routes(Routes__OSS                  )
        self.add_routes(Routes__Hacker_News__Cache   )

        Public_Data__Fast_API().setup().mount(self.app())       # available at /public-data/docs
        LLM_Cache__Fast_API  ().setup().mount(self.app())       # available at /llm-cache/docs
        RSS_Feeds__Fast_API  ().setup().mount(self.app())       # available at /rss-feeds/docs
        Admin__Fast_API      ().setup().mount(self.app())       # available at /admin/docs

    def path_static_folder(self):
        return path_combine(myfeeds_ai.path, 'static')

    def setup(self):
        self.setup_local_stack()
        super().setup()
        self.add_static_ui()
        return self


    def setup_local_stack(self):
        load_dotenv()
        if get_env('MY_FEEDS__USE_LOCALSTACK') == 'True':
            from osbot_aws.testing.Temp__Random__AWS_Credentials import Temp_AWS_Credentials
            from osbot_local_stack.local_stack.Local_Stack       import Local_Stack
            from osbot_utils.utils.Env                           import set_env

            DATA_FEEDS__TEST__AWS_ACCOUNT_ID = '000011110000'
            Temp_AWS_Credentials().set_vars()

            set_env('AWS_ACCOUNT_ID',DATA_FEEDS__TEST__AWS_ACCOUNT_ID)  # todo: fix the Temp_AWS_Credentials so that we don't need use this set_env

            print(f"------ using local stack with account id: {DATA_FEEDS__TEST__AWS_ACCOUNT_ID}-----")

            local_stack = Local_Stack().activate()
            return local_stack