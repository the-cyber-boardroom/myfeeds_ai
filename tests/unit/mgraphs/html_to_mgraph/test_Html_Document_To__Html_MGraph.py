from unittest                                                        import TestCase
from myfeeds_ai.mgraphs.html_to_mgraph.Html_Document_To__Html_MGraph import Html_Document_To__Html_MGraph
from osbot_utils.helpers.html.schemas.Schema__Html_Document          import Schema__Html_Document
from osbot_utils.helpers.safe_str.Safe_Str__Html                     import Safe_Str__Html
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import load_dotenv
from osbot_utils.utils.Http import GET
from tests._test_data.Sample_Test_Files                              import Sample_Test_Files

class test_Html_Document_To__Html_MGraph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html          = Sample_Test_Files().html_bootstrap_example()            # Load HTML sample
        #cls.html          = GET("https://docs.diniscruz.ai")
        #cls.html = GET("https://www.linkedin.com")

    def setUp(self):
        self.html_to_graph = Html_Document_To__Html_MGraph(html=self.html)
        self.create_png    = False

    def tearDown(self):
        if self.create_png:
            with self.html_to_graph.html_mgraph.screenshot() as _:
                load_dotenv()
                png_file = f"{self.__class__.__name__}.png"

                with _.export().export_dot() as dot:
                    dot.set_node__shape__type__box()
                    dot.set_node__shape__rounded()
                    dot.show_node__value()
                    #dot.show_node__id()

                _.save_to(png_file)
                _.dot()

    def test__init__(self):
        with self.html_to_graph as _:
            assert type(_) is Html_Document_To__Html_MGraph
            assert len(self.html) == 3085
            assert _.html         == self.html
            assert type(_.html)   is Safe_Str__Html
            assert "<title>Simple Bootstrap 5 Webpage</title>" in _.html

    def test_convert(self):
        with self.html_to_graph as _:
            _.convert()
            assert type(_.html__document) is Schema__Html_Document
            #pprint(_.html__dict)


    def test_convert__to__html_schema(self):
        with self.html_to_graph as _:
            _.convert__to__html_schema()
            assert type(_.html__document) is Schema__Html_Document

    def test_convert__simple_html(self):
        html = """\
<html>
    <body>
        <p>hello</p>
        <p>world</p>
    </body>
</html>"""
        print()
        self.html_to_graph = Html_Document_To__Html_MGraph(html=html)
        with self.html_to_graph as _:
            _.convert()


