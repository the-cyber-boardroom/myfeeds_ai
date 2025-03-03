from mgraph_db.mgraph.MGraph                                                        import MGraph
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File        import Hacker_News__File



class Hacker_News__MGraph(Hacker_News__File):
    mgraph    : MGraph
    extension : S3_Key__File_Extension  = S3_Key__File_Extension.MGRAPH__JSON

    def load(self):
        with self.hacker_news_storage as _:
            super().load()
            self.mgraph = type(self.mgraph).from_json__compressed(self.file_data)
        return self

    def save(self):
        with self.hacker_news_storage as _:
            saved__path_now   = _.save_to__now__mgraph   (mgraph=self.mgraph, file_id=self.file_id)
            save__path_latest = _.save_to__latest__mgraph(mgraph=self.mgraph, file_id=self.file_id)
            if saved__path_now != self.path_now():
                raise ValueError(f"in Hacker_News__MGraph.save, the saved__path_now was '{saved__path_now}' and it was expected to be '{self.path_now()}'")
            if save__path_latest != self.path_latest():
                raise ValueError(f"in Hacker_News__MGraph.save, the save__path_latest was '{save__path_latest}' and it was expected to be '{self.path_latest()}'")


