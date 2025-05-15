from mgraph_db.mgraph.MGraph                                    import MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Screenshot  import Html_MGraph__Screenshot


class Html_MGraph(MGraph):

    def html_mgraph__screenshot(self):
        return Html_MGraph__Screenshot(html_mgraph=self)

    def node__html(self):
        return self.values().get_by_value(value='html', value_type=str)
