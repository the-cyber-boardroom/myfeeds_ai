import pytest
import requests
from unittest                                             import TestCase
from osbot_utils.utils.Env                                import not_in_github_action
from myfeeds_ai.utils.Version                  import version__myfeeds_ai
from deploy.lambdas.Deploy_Lambda__MyFeeds_AI import Deploy_Lambda__MyFeeds_AI


class test__qa__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.deploy_lambda   = Deploy_Lambda__MyFeeds_AI()
        cls.lambda_function = cls.deploy_lambda.lambda_function
        cls.lambda_url      = cls.lambda_function.function_url()
        cls.session         = requests.Session()


    def requests_get(self, endpoint, params=None):
        response = self.session.get(f"{self.lambda_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response

    def test_raw_html_live(self):
        if not_in_github_action():
            pytest.skip("This test can only be executed in GH Actions after the deployment of the latest lambda")
        response = self.requests_get('info/version')
        assert response.status_code == 200
        assert response.json() == {'version': version__myfeeds_ai}