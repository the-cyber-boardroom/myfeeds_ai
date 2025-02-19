import pytest
from unittest                                           import TestCase
from osbot_aws.apis.shell.Http__Remote_Shell            import Http__Remote_Shell
from osbot_utils.utils.Env                              import get_env, load_dotenv

URL__LOCALHOST__MY_FEEDS_API       = "http://localhost:7777"
ENV_NAME__URL__DEV__MY_FEEDS__API  = "MY_FEEDS__DEV_API"

@pytest.mark.skip("only used for manual testing")
class test_remote_shell_lambda(TestCase):

    def setUp(self):
        load_dotenv()
        self.target_server = get_env(ENV_NAME__URL__DEV__MY_FEEDS__API, URL__LOCALHOST__MY_FEEDS_API)
        self.target_url = f'{self.target_server}/debug/lambda-shell'
        self.shell = Http__Remote_Shell(target_url=self.target_url)

    def test_0_lambda_shell_setup(self):
        assert self.shell.ping() == 'pong'


    def test_1_ping(self):
        def return_value():
            return 'here....'
        assert self.shell.function(return_value) == 'here....'

    def test_2_env_vars(self):
        def return_value():
            from osbot_utils.utils.Env import env_vars
            return env_vars()

        server_env_vars = self.shell.function(return_value)
        assert server_env_vars['AWS_ACCOUNT_ID'] == '000011110000'
