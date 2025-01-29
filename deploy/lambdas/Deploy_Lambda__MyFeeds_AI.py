from osbot_aws.apis.test_helpers.Temp_Aws_Roles import Temp_Aws_Roles
from osbot_utils.utils.Env                      import get_env, load_dotenv
from osbot_aws.AWS_Config                       import aws_config
from osbot_utils.type_safe.Type_Safe             import Type_Safe
from osbot_aws.deploy.Deploy_Lambda             import Deploy_Lambda
from myfeeds_ai.utils.Version                   import version__myfeeds_ai


class Deploy_Lambda__MyFeeds_AI(Type_Safe):
    lambda_name : str = 'myfeeds_ai'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_aws_credentials()
        self.deploy_lambda   = Deploy_Lambda(self.lambda_name)
        self.lambda_function = self.deploy_lambda.lambda_function()

    def deploy(self):
        #self.aws_setup()
        self.lambda_setup()
        self.deploy_lambda.deploy()
        self.lambda_setup_post_update()

    def invoke(self):
        with self.lambda_function as _:
            result = _.invoke()
            return result

    # def aws_setup(self):
    #     temp_aws_roles = Temp_Aws_Roles()
    #     if temp_aws_roles.for_lambda_invocation__not_exists():
    #         temp_aws_roles.for_lambda_invocation__create()

    def lambda_setup(self):
        self.deploy_lambda.set_container_image(self.ecr_image_uri())
        env_variables = {}
        self.deploy_lambda.set_env_variables(env_variables)

    def lambda_setup_post_update(self):
        with self.lambda_function as _:
            if _.function_url_exists() is False:
                _.function_url_create_with_public_access()



    def ecr_image_uri(self):
        account_id  = aws_config.account_id()
        region_name = aws_config.region_name()
        image_name  = self.lambda_name
        image_tag   = version__myfeeds_ai
        return f'{account_id}.dkr.ecr.{region_name}.amazonaws.com/{image_name}:{image_tag}'

    def setup_aws_credentials(self):
        load_dotenv()
        aws_config.set_aws_session_account_id (get_env('AWS_ACCOUNT_ID'       ))
        aws_config.set_region                 (get_env('AWS_DEFAULT_REGION'   ))
        aws_config.set_aws_access_key_id      (get_env('AWS_ACCESS_KEY_ID'    ))
        aws_config.set_aws_secret_access_key  (get_env('AWS_SECRET_ACCESS_KEY'))


if __name__ == '__main__':
    print("****************************************************")
    print("****   Deploy_Lambda__MyFeeds_AI    ****")
    print("****************************************************")
    print()
    with Deploy_Lambda__MyFeeds_AI() as _:
        print(f"... deploying lambda function: {_.lambda_name}")
        _.deploy()
        response = _.invoke()
        print(f"... invocation response: {response}")
        function_url = _.lambda_function.function_url()
        print(f"...you can try it at {function_url}")