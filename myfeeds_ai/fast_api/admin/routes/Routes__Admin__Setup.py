from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes


class Routes__Admin__Setup(Fast_API_Routes):
    tag: str = 'setup'

    def ping(self):
        return 'pong'

    def setup_routes(self):
        self.add_route_get(self.ping)
