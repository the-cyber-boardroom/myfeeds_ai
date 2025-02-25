from unittest                                                                                   import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_Articles  import Flow__Hacker_News__Process_Articles
from tests.integration.data_feeds__objs_for_tests                                               import cbr_website__assert_local_stack

class test__int__Flow__Hacker_News__Process_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()

    def setUp(self):
        self.process_articles = Flow__Hacker_News__Process_Articles()

    def test_run(self):

        # live_data = Hacker_News__Live_Data()
        # path      = "2025/02/19/22"
        # file_name = "feed-data.json"
        # files = Hacker_News__Files()
        # pprint(live_data.get_json(path, file_name))
        #kwargs = dict(year = "2025", month="02", day="19", hour="22")

        #pprint(files.feed_data__load_rss_and_parse().json())
        #pprint(files.feed_data__from_date(**kwargs).json())
        #return


        with self.process_articles as _:
            _.run()
            assert len(_.articles_to_process) == 50

