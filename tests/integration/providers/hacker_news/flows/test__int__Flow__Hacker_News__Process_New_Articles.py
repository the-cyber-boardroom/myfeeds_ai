from unittest import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_New_Articles import Flow__Hacker_News__Process_New_Articles

class test_Flow__Hacker_News__Process_New_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow_process_new_articles = Flow__Hacker_News__Process_New_Articles()
        #cls.path__timeline__current   = '2025/02/20/23/feed-timeline.mgraph.json'
        cls.path__timeline__current   = '2025/02/21/13/feed-timeline.mgraph.json'
        cls.path__timeline__previous  = '2025/02/19/22/feed-timeline.mgraph.json'
        with cls.flow_process_new_articles as _:
            _.new_articles.path__timeline__current  = cls.path__timeline__current
            _.new_articles.path__timeline__previous = cls.path__timeline__previous

    def test_process_flow(self):
        with self.flow_process_new_articles as _:
            result = self.flow_process_new_articles.run()

    def test_load_and_diff_timeline_data(self):
        with self.flow_process_new_articles as _:

            _.load_and_diff_timeline_data()                             # since we are using cached data , these will always be the ame
            assert _.timeline_diff is not None
            # assert json__equals__list_and_set(_.timeline_diff.json(), { 'added_values'  : {  type_full_name(Time_Chain__Day)   : [ '20'],
            #                                                                                  type_full_name(Time_Chain__Source): [ '272b4927', 'e5091ea4', '5d2f8952', 'ce7e697e',
            #                                                                                                                       'd54c06c4', '9153bba8', '55b2f8d2'            ]},
            #                                                             'removed_values': { type_full_name(Time_Chain__Day)    : [ '10'],
            #                                                                                 type_full_name(Time_Chain__Source) : [ '468bfcf6', 'f2082031', '08ec0110', 'ea2a87d4',
            #                                                                                                                        '0a68e403','d0ca70d4', '5f6bf957'             ]}}
            #                                  )

            # load_dotenv()
            #
            # assert type(_.timeline_diff) is Schema__MGraph__Diff__Values
            # #pprint(_.timeline_diff.json())
            # self.view = MGraph__View__Diff__Values(diff=_.timeline_diff)
            #
            # self.view.create_graph()
            # screenshot_file = type(self).__name__ + '.png'
            # with self.view.create_mgraph_screenshot() as _:
            #     # with _.export().export_dot() as dot:
            #     #     dot.show_node__value__key()
            #     _.save_to(screenshot_file)
            #     _.dot()

