from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values                          import Schema__MGraph__Diff__Values
from mgraph_db.mgraph.actions.MGraph__Diff__Values                                  import MGraph__Diff__Values
from mgraph_db.providers.time_chain.MGraph__Time_Chain                              import MGraph__Time_Chain
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types       import Time_Chain__Year, Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Live_Data import Hacker_News__Live_Data
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News     import FILE_ID__TIMELINE__DIFF, FILE_ID__TIMELINE__MGRAPH
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File        import Hacker_News__File

from osbot_utils.utils.Dev import pprint


class Hacker_News__File__Timeline__Diff(Hacker_News__File):
    file_id               = FILE_ID__TIMELINE__DIFF
    extension             = S3_Key__File_Extension.JSON
    hacker_news_live_data : Hacker_News__Live_Data
    timeline_diff         : Schema__MGraph__Diff__Values    = None

    def create(self, previous_path, current_path):
        file_name                  = self.file_name__feed_timeline_mgraph()
        data__timeline_current     = self.hacker_news_live_data.get_json(current_path , file_name)              # todo: review the use live data to get this data (at the moment it is the only location where we have this data))
        data__timeline_previous    = self.hacker_news_live_data.get_json(previous_path, file_name)
        mgraph__timeline__current  = MGraph__Time_Chain.from_json__compressed(data__timeline_current )
        mgraph__timeline__previous = MGraph__Time_Chain.from_json__compressed(data__timeline_previous)

        differ = MGraph__Diff__Values(graph1=mgraph__timeline__current ,
                                      graph2=mgraph__timeline__previous)

        self.timeline_diff = differ.compare([ Time_Chain__Year,Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source])
        return self

    def load(self):
        json_data = super().load()
        if json_data:
            self.timeline_diff = Schema__MGraph__Diff__Values.from_json(json_data)
            return self.timeline_diff

    def save(self):
        if self.timeline_diff:
            self.file_data = self.timeline_diff.json()
            super().save()

    def file_name__feed_timeline_mgraph(self):
        return f"{FILE_ID__TIMELINE__MGRAPH}.{S3_Key__File_Extension.MGRAPH__JSON.value}"