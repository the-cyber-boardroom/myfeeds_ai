from mgraph_db.mgraph.MGraph                                                            import MGraph
from myfeeds_ai.providers.cyber_security.owasp.actions.Owasp__Files__Top_10             import Owasp__Files__Top_10
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category          import Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Schema__Owasp__Top_10__Category  import Schema__Owasp__Top_10__Category

from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import load_dotenv


class MGraph__Owasp__Top_10__Category(Type_Safe):
    files_top_10: Owasp__Files__Top_10
    category     : Owasp__Top_10__Category
    mgraph       : MGraph
    save_png     : bool

    def build(self):
        raw_data  = self.raw_data_json()
        #pprint(raw_data.json())
        with self.mgraph.builder() as _:
            _.add_node(raw_data.name)
            _.connect_to('description').connect_to('intro').connect_to(raw_data.description.intro[0:40])
            for item in raw_data.description.items:
                _.connect_to(item[0:40]).up()
            pass
        #return self.mgraph.export().export_tree_values().as_text()


    def raw_data_json(self) -> Schema__Owasp__Top_10__Category:
        return self.files_top_10.raw_data__json(self.category)

    def screenshot(self):
        with self.mgraph.screenshot() as _:
            with _.export().export_dot() as dot:
                dot.set_graph__rank_dir__lr()
                dot.set_node__shape__type__box()
                dot.set_node__shape__rounded()
                #dot.show_edge__type()
                dot.show_edge__predicate__str()

            load_dotenv()
            if self.save_png:
                _.save_to(f'{self.__class__.__name__}.png')
            _.show_node_value()
            png_bytes = _.dot()
            return png_bytes
