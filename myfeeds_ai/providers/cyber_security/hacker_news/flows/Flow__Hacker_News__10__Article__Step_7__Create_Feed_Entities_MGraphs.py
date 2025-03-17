from typing                                                                                             import List, Dict
from mgraph_db.mgraph.MGraph                                                                            import MGraph
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Feed__Text_Entities           import Hacker_News__Feed__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage                       import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Text_Entities                 import Hacker_News__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current         import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                      import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change      import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step                import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                     import Flow
from osbot_utils.helpers.flows.decorators.flow                                                          import flow
from osbot_utils.helpers.flows.decorators.task                                                          import task
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe


FLOW__HACKER_NEWS__7__MAX__ARTICLES_TO_MOVE = 1

class Flow__Hacker_News__10__Article__Step_7__Create_Feed_Entities_MGraphs(Type_Safe):
    file_articles_current                    : Hacker_News__File__Articles__Current
    articles_to_process                      : List[Schema__Feed__Article                ]
    feed_text_entities                       : Hacker_News__Feed__Text_Entities
    storage                                  : Hacker_News__Storage
    target                                   : str                         = '/tmp/feed-entities.mgraph-both.json'
    max_articles_to_move                     : int = FLOW__HACKER_NEWS__7__MAX__ARTICLES_TO_MOVE
    output                                   : dict
    from_step                                : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__7__MERGE__FEED_ENTITIES_GRAPHS
    to_step                                  : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__8__CREATE__FEED_ENTITIES_TREE_VIEW
    status_changes                           : List[Schema__Feed__Article__Status__Change]
    mgraph_entities                          : MGraph
    mgraph_entities__titles                  : MGraph
    mgraph_entities__descriptions            : MGraph
    path_latest__text_entities               : str
    path_latest__text_entities__titles       : str
    path_latest__text_entities__descriptions : str
    path_now__text_entities                  : str
    path_now__text_entities__titles          : str
    path_now__text_entities__descriptions    : str


    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__7__merge_day_entities_graphs()

    @task()
    def task__2__create_file_with_feed_text_entities_mgraph(self):
        files_to_process__titles              = []
        files_to_process__descriptions        = []
        #file__feed_text_entities              = self.feed_text_entities.file__feed_text_entities             ()        # todo: (to wire back in ) don't create the text entities for both title and description
        file__feed_text_entities_titles       = self.feed_text_entities.file__feed_text_entities_titles      ()         # for now only generate the text entities for the title # todo: review performance since it is taking a bit to create these (about 4 secs each)
        #file__feed_text_entities_descriptions = self.feed_text_entities.file__feed_text_entities_descriptions()        # todo: (to wire back in ) don't create the text entities for both description

        # we always need to refresh this since by the fact that we are here, there are one or more articles to update
        with self.file_articles_current as _:
            for article_id, article in _.articles.articles.items():
                if article.path__file__text_entities__title__mgraph:
                   files_to_process__titles.append((article_id,article.path__file__text_entities__title__mgraph ))
                if article.path__file__text_entities__description__mgraph:
                    files_to_process__descriptions.append((article_id,article.path__file__text_entities__description__mgraph))

        #text_entities               = Hacker_News__Text_Entities(mgraph_entities=self.mgraph_entities              ).setup()
        text_entities__titles       = Hacker_News__Text_Entities(mgraph_entities=self.mgraph_entities__titles      ).setup()
        #text_entities__descriptions = Hacker_News__Text_Entities(mgraph_entities=self.mgraph_entities__descriptions).setup()

        for (article_id, file_to_process) in files_to_process__titles:                  # this will process all 50 files (if there is a need to process less files, this is where we can control it)
            json_data         = self.storage.path__load_data(file_to_process)
            mgraph_to_process = MGraph.from_json(json_data)
            text_entities__titles.add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_to_process)
            #text_entities        .add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_to_process)

        # for (article_id, file_to_process) in files_to_process__descriptions:            # and here (control how many articles are processed)
        #     json_data         = self.storage.path__load_data(file_to_process)
        #     mgraph_to_process = MGraph.from_json(json_data)
        #     text_entities__descriptions.add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_to_process)
        #     text_entities              .add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_to_process)

        #file__feed_text_entities             .save_data(text_entities              .mgraph_entities.json())
        file__feed_text_entities_titles      .save_data(text_entities__titles      .mgraph_entities.json())
        #file__feed_text_entities_descriptions.save_data(text_entities__descriptions.mgraph_entities.json())

        #self.path_latest__text_entities               = file__feed_text_entities             .path_latest()
        self.path_latest__text_entities__titles       = file__feed_text_entities_titles      .path_latest()
        #self.path_latest__text_entities__descriptions = file__feed_text_entities_descriptions.path_latest()
        #self.path_now__text_entities                  = file__feed_text_entities             .path_now   ()             # note that this is on the hour folder NOT on the article folder
        self.path_now__text_entities__titles          = file__feed_text_entities_titles      .path_now   ()             #      since at the moment there is only support for saving on both "hour now" and latest
        #self.path_now__text_entities__descriptions    = file__feed_text_entities_descriptions.path_now   ()             #      but not on "article now" and latest

    def task__3__move_articles_to_next_step(self):
        for article in self.articles_to_process[0:self.max_articles_to_move]:
            article.next_step                                     = self.to_step
            article_change_status                                 = Schema__Feed__Article__Status__Change(article=article, from_step=self.from_step)
            article.path__file__feed__text_entities               =  self.path_now__text_entities
            article.path__file__feed__text_entities__titles       =  self.path_now__text_entities__titles
            article.path__file__feed__text_entities__descriptions =  self.path_now__text_entities__descriptions
            self.status_changes.append(article_change_status)

        self.file_articles_current.save()


    # def task__3__create_png_for_feed_text_entities_mgraph(self):
    #
    #     with print_duration(action_name='create json'):
    #         json_data = json_file_load(path=self.target)
    #         mgraph_entities = MGraph.from_json(json_data)
    #         text_entities = Hacker_News__Text_Entities(mgraph_entities=mgraph_entities)
    #
    #         pprint(text_entities.mgraph_entities.data().stats())
    #     with print_duration(action_name='create png'):
    #         png_file = self.target + ".png"
    #         #text_entities.screenshot__setup()
    #         with text_entities.screenshot().export().export_dot() as _:
    #             _.show_node__value()
    #             _.show_edge__predicate()
    #             _.set_node__shape__type__box()
    #             _.set_graph__layout_engine__sfdp()
    #             #_.set_graph__rank_dir__lr()
    #         text_entities.screenshot().save_to(png_file).dot()
    #
    #         #pprint(file_size(png_file))

    def task__4__create_output(self):
        self.output = dict(articles_to_process                      = len(self.articles_to_process)                     ,
                           mgraph_entities                          = self.mgraph_entities              .data().stats() ,
                           mgraph_entities__titles                  = self.mgraph_entities__titles      .data().stats() ,
                           mgraph_entities__descriptions            = self.mgraph_entities__descriptions.data().stats() ,
                           path_latest__text_entities               = self.path_latest__text_entities                   ,
                           path_latest__text_entities__titles       = self.path_latest__text_entities__titles           ,
                           path_latest__text_entities__descriptions = self.path_latest__text_entities__descriptions     ,
                           path_now__text_entities                  = self.path_now__text_entities                      ,
                           path_now__text_entities__titles          = self.path_now__text_entities__titles              ,
                           path_now__text_entities__descriptions    = self.path_now__text_entities__descriptions        ,
                           max_articles_to_move                     = self.max_articles_to_move                         ,
                           status_changes                           = self.status_changes.json()                        )


    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process                   ()
            _.task__2__create_file_with_feed_text_entities_mgraph ()
            _.task__3__move_articles_to_next_step                 ()
            _.task__4__create_output                              ()
        return self.output

    def run(self):
        return self.process_articles().execute_flow()

