from osbot_fast_api.api.Fast_API_Routes  import Fast_API_Routes
from myfeeds_ai.utils.Version import version__myfeeds_ai

ROUTES_TAG__INFO   = 'info'
ROUTES_PATHS__INFO = [f'/{ROUTES_TAG__INFO}/version']


class Routes__Info(Fast_API_Routes):
    tag :str = ROUTES_TAG__INFO

    def version(self):
        return {'version': version__myfeeds_ai}

    def setup_routes(self):
        self.add_route_get(self.version)

