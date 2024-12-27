from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes


class Routes__RSS_Parser(Fast_API_Routes):
    tag : str = 'rss-parser'

    def ping(self):
        return {'it is':  'pong'}

    def setup_routes(self):
        self.add_route_get(self.ping)