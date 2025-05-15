from unittest                                                                   import TestCase
from myfeeds_ai.mgraphs.html_to_mgraph.Html_Document__To__Html_MGraph__Schema   import Html_Document__To__Html_MGraph__Schema
from osbot_utils.helpers.html.Html__To__Html_Document                           import Html__To__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Document                     import Schema__Html_Document
from osbot_utils.utils.Env                                                      import load_dotenv
from tests.unit.mgraphs.html_to_mgraph.test_Html_Document__To__Html_MGraph      import HTML__EXAMPLE__WITH__FORM


class test_Html_Document__To__Html_MGraph__Schema(TestCase):
    def setUp(self):
        self.html           = HTML__EXAMPLE__WITH__FORM
        self.title          = "Html Graph"
        self.html_document  = Html__To__Html_Document(html=self.html).convert()
        self.html_to_schema = Html_Document__To__Html_MGraph__Schema(html_document=self.html_document)
        self.create_png     = False

    def test__init__(self):
        with self.html_to_schema as _:
            assert type(_)                is Html_Document__To__Html_MGraph__Schema
            assert len(self.html)         == 421
            assert _.html_document        == self.html_document
            assert type(_.html_document)  is Schema__Html_Document

    def test_convert(self):
        with self.html_to_schema as _:
            _.convert()
            assert _.html_mgraph.data().stats() == {'edges_ids': 8, 'nodes_ids': 9}

    def test_screenshot(self):
        if self.create_png:
            load_dotenv()
            target_file = f'{self.__class__.__name__}.png'
            with self.html_to_schema as _:
                _.convert()
                png_bytes = _.screenshot(target_file=target_file)
                assert len(png_bytes) > 10000

    def test_tree_values(self):
        with self.html_to_schema as _:
            _.convert()
            assert _.tree_values() == ('html\n'
                                       '    head\n'
                                       '        title\n'
                                       '    body\n'
                                       '        h1\n'
                                       '        form\n'
                                       '            p\n'
                                       '                input\n'
                                       '                textarea')