from osbot_fast_api.api.Fast_API                                    import Fast_API
from myfeeds_ai.fast_api.public_data.routes.Routes__LLM_Cache__Data import Routes__LLM_Cache__Data

ROUTES__BASE_PATH__LLM_CACHE = '/llm-cache'

class LLM_Cache__Fast_API(Fast_API):
    base_path = ROUTES__BASE_PATH__LLM_CACHE

    def setup_routes(self):
        self.add_routes(Routes__LLM_Cache__Data  )
