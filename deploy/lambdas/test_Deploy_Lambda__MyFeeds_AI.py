from unittest                                  import TestCase
from myfeeds_ai.utils.Version                  import version__myfeeds_ai
from deploy.lambdas.Deploy_Lambda__MyFeeds_AI  import Deploy_Lambda__MyFeeds_AI


class test_Deploy_Lambda__MyFeeds_AI(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.deploy_lambda = Deploy_Lambda__MyFeeds_AI()

    def test_deploy_lambda(self):
        with self.deploy_lambda as _:
            result = _.lambda_deploy()
            assert result == {'body': 'Hello from Docker Lambda!', 'statusCode': 200}

    def test_ecr_image_uri(self):
        with self.deploy_lambda as _:
            ecr_image_uri = _.ecr_image_uri()       # todo: change values below to aws_config.account_id() and aws_config.region_name()
            assert ecr_image_uri == f'774305572074.dkr.ecr.eu-west-2.amazonaws.com/osbot_flows:{version__myfeeds_ai}'
