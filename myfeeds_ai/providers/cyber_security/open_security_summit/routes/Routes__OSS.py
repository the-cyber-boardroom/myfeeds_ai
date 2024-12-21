from osbot_fast_api.api.Fast_API_Routes                                                     import Fast_API_Routes
from starlette.responses                                                                    import PlainTextResponse
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Events        import OSS__Events
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Files         import OSS__Files
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Http_Content  import OSS__Http_Content
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Prompts       import OSS__Prompts

ROUTE_PATH__OSS   = 'open-security-summit'
ROUTES_PATHS__OSS = [ f'/{ROUTE_PATH__OSS}/all-data'                 ,
                      f'/{ROUTE_PATH__OSS}/all-files'                ,
                      f'/{ROUTE_PATH__OSS}/current-event-data'       ,
                      f'/{ROUTE_PATH__OSS}/current-event-prompt'     ,
                      f'/{ROUTE_PATH__OSS}/current-event-prompt-text',
                      f'/{ROUTE_PATH__OSS}/latest-versions'          ,
                      f'/{ROUTE_PATH__OSS}/raw-data'                 ]


class Routes__OSS(Fast_API_Routes):
    tag         : str                       = ROUTE_PATH__OSS
    http_content: OSS__Http_Content
    files       : OSS__Files
    events      : OSS__Events
    prompts     : OSS__Prompts

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.files.s3_db.setup()            # todo: refactor this to a better place (we need this to make sure the db is setup, and the s3 bucket created)


    def all_data(self):
        return self.files.content__current()

    def all_files(self):
        return self.files.all_files()

    def current_event_data(self):
        return self.events.current_event()

    def current_event_prompt(self):
        return self.files.current_event_prompt().json()

    def current_event_prompt_text(self, refresh=False):
        prompt_text  = self.files.current_event_prompt(refresh=refresh).prompt_text
        return PlainTextResponse(prompt_text)

    def latest_versions(self):
        return self.files.latest_versions()

    def raw_data(self):
        return self.files.raw_content__current().json()

    def setup_routes(self):
        self.add_route_get(self.all_data                 )
        self.add_route_get(self.all_files                )
        self.add_route_get(self.current_event_data       )
        self.add_route_get(self.current_event_prompt     )
        self.add_route_get(self.current_event_prompt_text)
        self.add_route_get(self.latest_versions          )
        self.add_route_get(self.raw_data                 )