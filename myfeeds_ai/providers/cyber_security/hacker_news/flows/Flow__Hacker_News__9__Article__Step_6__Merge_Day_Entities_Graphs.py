from typing                                                                                         import List, Dict
from mgraph_db.mgraph.MGraph                                                                        import MGraph
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Day                       import Hacker_News__Day
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage                   import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Text_Entities             import Hacker_News__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                  import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change  import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from osbot_utils.helpers.Obj_Id                                                                     import Obj_Id
from osbot_utils.helpers.flows.Flow                                                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                                                      import flow
from osbot_utils.helpers.flows.decorators.task                                                      import task
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                                              import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.utils.Threads                                                                      import execute_in_thread_pool

FLOW__HACKER_NEWS__9__MAX__GRAPHS_TO_MERGE          = 1
FILE_NAME__TEXT_ENTITIES__MGRAPH_JSON               = 'text-entities.mgraph.json'
FILE_NAME__TEXT_ENTITIES__TITLE__MGRAPH_JSON        = 'text-entities-title.mgraph.json'
FILE_NAME__TEXT_ENTITIES__DESCRIPTION__MGRAPH_JSON  = 'text-entities-description.mgraph.json'

class Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs(Type_Safe):
    file_articles_current       : Hacker_News__File__Articles__Current
    storage                     : Hacker_News__Storage
    output                      : dict
    articles_to_process         : List[Schema__Feed__Article                ]
    status_changes              : List[Schema__Feed__Article__Status__Change]
    max_graphs_to_merge         : int = FLOW__HACKER_NEWS__9__MAX__GRAPHS_TO_MERGE
    from_step                   : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__6__MERGE__DAY_ENTITIES_GRAPHS
    to_step                     : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__7__MERGE__FEED_ENTITIES_GRAPHS
    article_ids_to_process      : Dict[Obj_Id, Hacker_News__Day]
    hacker_news__days           : Dict[Safe_Str__File__Path, Hacker_News__Day]
    paths_hacker_news__days     : List[Safe_Str__File__Path]
    paths_hacker_news__days_pngs: List[Safe_Str__File__Path]
    days_processed              : set[Safe_Str__File__Path]
    days_skipped                : set[Safe_Str__File__Path]
    articles_processed          : set[Obj_Id]
    articles_skipped            : set[Obj_Id]
    files_in_day                : dict
    text_entities               : Dict[Safe_Str__File__Path, Hacker_News__Text_Entities]

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__6__merge_day_entities_graphs()

    @task()
    def task__2__find_days_to_process(self):
        for article in self.articles_to_process[0:self.max_graphs_to_merge]:
            article_id          = article.article_id
            path_folder_data    = article.path__folder__data

            hacker_news__day         = Hacker_News__Day(path__folder__data=path_folder_data)
            file_merged_day_entities = hacker_news__day.file_merged_day_entities__load()
            if True or article_id not in file_merged_day_entities.articles_ids:
                self.articles_processed.add(article_id)
                self.article_ids_to_process[article_id] = hacker_news__day
            else:
                self.articles_skipped.add(article_id)


    @task()
    def task__3__llm__merge_day_entities_graphs(self):
        calls    = [((), dict(article_id=article_id, hacker_news__day=hacker_news__day)) for article_id,hacker_news__day in self.article_ids_to_process.items()]               # args and kwargs (args need to be tuple)

        execute_in_thread_pool(self.task__3a__llm__merge_day_entities_graphs, calls=calls, max_workers=10)

    def task__3a__llm__merge_day_entities_graphs(self, article_id, hacker_news__day: Hacker_News__Day):
        path_to_day = hacker_news__day.path__folder__data
        if path_to_day not in self.days_processed:
            self.days_processed.add(path_to_day)
        else:
            self.days_skipped.add(path_to_day)
            return

        hacker_news__day.file_merged_day_entities().delete__now()
        merged_day_entities = hacker_news__day.file_merged_day_entities__load()
        mgraph_entities     = merged_day_entities.mgraph_entities
        text_entities       = Hacker_News__Text_Entities(mgraph_entities=mgraph_entities).setup()

        files_in_day     = self.storage.files_in__path(path_to_day, include_sub_folders=True)               # todo: look at the fact that this is returning s3_keys instead of s3_paths (i.e. this is retuning the full path)
        files_to_process = []
        for file_in_day in files_in_day:
            if file_in_day.endswith(FILE_NAME__TEXT_ENTITIES__TITLE__MGRAPH_JSON):
                files_to_process.append(Safe_Str__File__Path(file_in_day))
            if file_in_day.endswith(FILE_NAME__TEXT_ENTITIES__DESCRIPTION__MGRAPH_JSON):
                files_to_process.append(Safe_Str__File__Path(file_in_day))

        with text_entities as _:
            for s3_key in files_to_process:
                print(f'processing file: {s3_key}')
                if True or s3_key not in merged_day_entities.files_loaded:
                    s3_key__article_id = Obj_Id(s3_key.split('/')[7])                                              # todo: figure out where to get the article_id from the contents of the s3_key graph
                    json_data          = self.storage.s3_db.s3_file_data(s3_key)                                    # todo: refactor this so that we don't use the s3_db object
                    mgraph_to_process  = MGraph.from_json(json_data)
                    _.add_text_entities_mgraph(article_id=s3_key__article_id, mgraph_text_entities=mgraph_to_process)

                    merged_day_entities.files_loaded.add(s3_key)
                    merged_day_entities.articles_ids.add(s3_key__article_id)

        file_merged_day_entities = hacker_news__day.file_merged_day_entities()
        file_merged_day_entities.save_data(merged_day_entities.json())
        self.paths_hacker_news__days.append(Safe_Str__File__Path(Safe_Str__File__Path(file_merged_day_entities.path_now())))
        self.hacker_news__days[path_to_day] = hacker_news__day
        self.text_entities    [path_to_day] = text_entities

    # todo: add parallel execution to this task
    @task()
    def task__4__create_mgraph_png(self):
        for path_to_day, text_entities in self.text_entities.items():
            hacker_news_day               = self.hacker_news__days[path_to_day]
            file_merged_day_entities__png = hacker_news_day.file_merged_day_entities__png()
            text_entities.screenshot__setup()
            text_entities.screenshot().export().export_dot().set_graph__layout_engine__sfdp() # use SFDP layout
                                                                # .set_graph__rank_dir__lr() # use LR layout (Left to Right)
            png_bytes  = text_entities.screenshot().dot()
            file_merged_day_entities__png.save_data(png_bytes)
            self.paths_hacker_news__days_pngs.append(Safe_Str__File__Path(file_merged_day_entities__png.path_now()))

    def task__5__update_file_articles(self):
        with self.file_articles_current as _:
            _.load()
            articles_ids = self.articles_processed | self.articles_skipped
            for article_id in articles_ids:
                article = self.file_articles_current.article(article_id)
                article.path__file__day__text_entities                   = f"{article.path__folder__data}/text-entities-day.json"           # todo: refactor this to not use this hardcoded path (this should be using the file_* object)
                article.path__file__day__text_entities__png              = f'{article.path__folder__data}/text-entities-day.mgraph.png'
                article.next_step = self.to_step
                article_change_status = Schema__Feed__Article__Status__Change(article=article, from_step=self.from_step)
                self.status_changes.append(article_change_status)

            _.save()

    def task__6__create_output(self):
        stats__day_mgraphs = {}
        for path_to_day, text_entities in self.text_entities.items():
            stats__day_mgraphs[path_to_day] = text_entities.mgraph_entities.data().stats()
        hacker_news_days = {}
        for path_to_day, hacker_news__day in  self.hacker_news__days.items():
            with hacker_news__day.file_merged_day_entities__load() as _:
                hacker_news_days[path_to_day] = dict(articles_ids = _.articles_ids.json(),
                                                     files_loaded = _.files_loaded.json(),
                                                     mgraph_stats = _.mgraph_entities.data().stats(),
                                                     )

        self.output = dict(articles_to_process          = len(self.articles_to_process)          ,
                           articles_processed           = self.articles_processed          .json(),
                           articles_skipped             = self.articles_skipped            .json(),
                           hacker_news_days             = hacker_news_days                        ,
                           days_processed               = self.days_processed              .json(),
                           days_skipped                 = self.days_skipped                .json(),
                           paths_hacker_news__days      = self.paths_hacker_news__days     .json(),
                           paths_hacker_news__days_pngs = self.paths_hacker_news__days_pngs.json(),
                           stats__day_mgraphs           = stats__day_mgraphs                      ,
                           status_changes               =  self.status_changes             .json())

    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process      ()
            _.task__2__find_days_to_process          ()
            _.task__3__llm__merge_day_entities_graphs()
            _.task__4__create_mgraph_png             ()
            _.task__5__update_file_articles          ()
            _.task__6__create_output                 ()
        return self.output

    def run(self):
        return self.process_articles().execute_flow()