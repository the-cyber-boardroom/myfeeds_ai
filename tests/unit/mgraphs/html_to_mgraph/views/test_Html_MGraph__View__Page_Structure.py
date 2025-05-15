from unittest                                                                   import TestCase
from myfeeds_ai.mgraphs.html_to_mgraph.Html_Document__To__Html_MGraph           import Html_Document__To__Html_MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.views.Html_MGraph__View__Page_Structure  import Html_MGraph__View__Page_Structure
from osbot_utils.helpers.html.Html__To__Html_Document                           import Html__To__Html_Document
from osbot_utils.utils.Env                                                      import load_dotenv
from tests.unit.mgraphs.html_to_mgraph.test_Html_Document__To__Html_MGraph      import HTML__EXAMPLE__WITH__FORM, HTML__EXAMPLE__WITH__BOOTSTRAP

class test_Html_MGraph__View__Page_Structure(TestCase):
    # add support for using data from S3
    @classmethod
    def setUpClass(cls):
        cls.html                = HTML__EXAMPLE__WITH__FORM
        cls.html                = HTML__EXAMPLE__WITH__BOOTSTRAP
        cls.html_document       = Html__To__Html_Document       (html          = cls.html         ).convert()
        cls.html_mgraph         = Html_Document__To__Html_MGraph (html_document = cls.html_document).convert()
        #cls.mgraph_json_file    = './html_graph.json'                                              # use this cached version if we want to make sure the Ids area always the same
        #json_file_create(mgraph_json, path=cls.mgraph_json_file)
        #cls.html_mgraph         = Html_MGraph.from_json(json_file_load(cls.mgraph_json_file))
        cls.view_page_structure = Html_MGraph__View__Page_Structure(html_mgraph=cls.html_mgraph, create_png=True)
        cls.create_png          = False


    def tearDown(self):
        if self.create_png:
            load_dotenv()
            self.view_page_structure.create_screenshot()


    def test_create_using_query(self):
        with self.view_page_structure as _:
            _.create_using_mquery()


