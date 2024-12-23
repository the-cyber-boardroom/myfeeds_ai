from osbot_fast_api.api.Fast_API                                        import Fast_API
from myfeeds_ai.fast_api.public_data.routes.Routes__Public__Hacker_News import Routes__Public__Hacker_News

ROUTES__BASE_PATH__PUBLIC_DATA = '/public-data'

class Public_Data__Fast_API(Fast_API):
    base_path = ROUTES__BASE_PATH__PUBLIC_DATA

    def setup_routes(self):
        self.add_routes(Routes__Public__Hacker_News)