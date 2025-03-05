from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types                   import Time_Chain__Source
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__New     import Hacker_News__File__Articles__New
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Timeline__Diff    import Hacker_News__File__Timeline__Diff
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles             import Schema__Feed__Article
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.helpers.flows.Flow                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                  import flow
from osbot_utils.helpers.flows.decorators.task                                                  import task
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe

class Flow__Hacker_News__3__Extract_New_Articles(Type_Safe):
    file_timeline_diff    : Hacker_News__File__Timeline__Diff
    file_current_articles : Hacker_News__File__Articles__Current
    file_new_articles     : Hacker_News__File__Articles__New
    current__path         : str = None
    previous__path        : str = None
    output                : dict

    @task()
    def task__1__resolve__previous__path(self):
        new_articles = self.file_new_articles.load()  # get latest version
        if not self.previous__path:
            self.previous__path = new_articles.path__current
        if not self.current__path:
            self.current__path =  self.file_new_articles.hacker_news_storage.path__folder_now()

    @task()
    def task__2__create__timeline_diff(self):
        with self.file_timeline_diff as _:
            if _.not_exists():
                _.create(previous_path=self.previous__path, current_path=self.current__path)
                _.save()
            else:
                _.load()

    @task()
    def task__3__save__new_articles(self):
        timeline_diff = self.file_timeline_diff.timeline_diff
        if self.current__path and timeline_diff:

            data = dict(path__current    = self.current__path  ,
                        path__previous   = self.previous__path ,
                        timeline_diff    = timeline_diff       )
            self.file_new_articles.save_data(data)


    @task()
    def task__4__update_current_articles(self):
        timeline_diff = self.file_timeline_diff.timeline_diff
        if timeline_diff:
            with self.file_current_articles as _:
                current_articles     = _.load()
                new_articles_ids     = timeline_diff.added_values  .get(Time_Chain__Source, set())
                removed_articles_ids = timeline_diff.removed_values.get(Time_Chain__Source, set())

                for new_article_id in new_articles_ids:
                    kwargs          = dict(path__folder__source = self.current__path, article_id= new_article_id)
                    current_article = Schema__Feed__Article(**kwargs)
                    if Obj_Id(new_article_id) not in current_articles.articles:
                        current_articles.articles[Obj_Id(new_article_id)] = current_article

                for removed_article_id in removed_articles_ids:
                    if Obj_Id(removed_article_id) in current_articles.articles:
                        del current_articles.articles[Obj_Id(removed_article_id)]

                _.save()

    @task()
    def task__5__create_output(self):
        self.output = dict(path_previous         = self.previous__path               ,
                           path_current          = self.current__path                ,
                           file_timeline_diff    = self.file_timeline_diff.info    (),
                           file_current_articles = self.file_current_articles.info (),
                           file_new_articles     = self.file_new_articles.info     ())

    @flow()
    def extract_new_articles(self) -> Flow:
        with self as _:
            _.task__1__resolve__previous__path           ()
        if self.current__path == self.previous__path:
            return {'error': { 'source'       :'current__path == previous_path',
                               'current__path': self.current__path,
                               'previous__path': self.previous__path}}
        with self as _:
            _.task__2__create__timeline_diff          ()
            _.task__3__save__new_articles             ()
            _.task__4__update_current_articles        ()
            _.task__5__create_output                  ()
        return self.output

    def run(self):
        return self.extract_new_articles().execute_flow()