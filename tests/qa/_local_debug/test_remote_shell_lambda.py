import pytest
from unittest                                           import TestCase
from osbot_aws.apis.shell.Http__Remote_Shell            import Http__Remote_Shell
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env                              import get_env, load_dotenv

URL__LOCALHOST__MY_FEEDS_API       = "http://localhost:7777"
ENV_NAME__URL__DEV__MY_FEEDS__API  = "URL__DEV__MY_FEEDS__API"

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

    # def test__local_server__env_vars(self):
    #     def return_value():
    #         from osbot_utils.utils.Env import env_vars
    #         return env_vars()
    #
    #     server_env_vars = self.shell.function(return_value)
    #     assert server_env_vars['AWS_ACCOUNT_ID'] == '000011110000'

    def test__dev_server__check_version(self):
        def server_version():
            from myfeeds_ai.utils.Version import version__myfeeds_ai
            return version__myfeeds_ai

        from myfeeds_ai.utils.Version import version__myfeeds_ai
        assert self.shell.function(server_version) == version__myfeeds_ai

    def test__dev_server__flow_process_rss(self):

        def flow_process_rss():
            from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_RSS import Flow__Hacker_News__1__Process_RSS
            #process_rss  = Flow__Hacker_News__Process_RSS()
            #return_value = process_rss.run().flow_return_value
            from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Create_MGraph__Articles__Timeline import Flow__Hacker_News__2__Create_Articles_Timeline
            from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                                         import Hacker_News__Files
            flow_timeline = Flow__Hacker_News__2__Create_Articles_Timeline()
            files         =  Hacker_News__Files()
            data_feed     = files.feed_data__load_rss_and_parse()
            data_feed.feed_data.articles = data_feed.feed_data.articles[0:10]
            #return f"{len(data_feed.feed_data.articles)}"
            flow_timeline.setup(data_feed=data_feed)
            #return_value  = flow_timeline.execute_flow()#.flow_return_value
            #flow_timeline.main(data_feed=data_feed)
            from osbot_utils.helpers.duration.decorators.capture_duration import capture_duration
            with capture_duration() as duration:
                with flow_timeline as _:
                    _.data_feed = data_feed
                    _.load_articles()
                    _.create_mgraph()
                    _.save_mgraph()
                    #_.create_dot_code()
                    with _.mgraph_timeseries.screenshot() as screenshot:
                        return screenshot.export().to__dot()
                    _.map_durations()
            # flow_timeline.flow_config.logging_enabled = True
            # from osbot_utils.testing.Stdout import Stdout
            # with Stdout() as stdout:
            #     flow_timeline.print_log_messages()

            return_value = flow_timeline.durations
            return_value['_duration'] = duration.seconds
            return return_value

        result = self.shell.function(flow_process_rss)

        pprint(result)
