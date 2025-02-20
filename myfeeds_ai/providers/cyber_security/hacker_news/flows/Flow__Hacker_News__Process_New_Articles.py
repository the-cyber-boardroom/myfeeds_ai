from osbot_utils.helpers.flows.Flow             import Flow
from osbot_utils.helpers.flows.decorators.flow  import flow
from osbot_utils.type_safe.Type_Safe            import Type_Safe


class Flow__Hacker_News__Process_New_Articles(Type_Safe):
    output : dict

    def create_output(self):
        return {}


    @flow()
    def process_rss(self) -> Flow:
        with self as _:
            # _.fetch_rss_feed()
            # _.create_timeline()
            # _.save_timeline()
            # _.invalidate_cache()
            _.create_output()

        return self.output

    def run(self):
        return self.process_rss().execute_flow()