from osbot_aws.apis.shell.Lambda_Shell  import Lambda_Shell, SHELL_VAR
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from fastapi                            import Request

ROUTES__EXPECTED_PATHS__DEBUG = ['/debug/lambda-shell']

class Routes__Debug(Fast_API_Routes):
    tag : str = 'debug'

    async def lambda_shell(self, request: Request):
        data = await request.json()
        if data:
            shell_server = Lambda_Shell(data.get(SHELL_VAR))
            if shell_server.valid_shell_request():
                return shell_server.invoke()
        return '...this is not the lambda shell you are looking for ....'


    def setup_routes(self):
        self.add_route_post(self.lambda_shell)