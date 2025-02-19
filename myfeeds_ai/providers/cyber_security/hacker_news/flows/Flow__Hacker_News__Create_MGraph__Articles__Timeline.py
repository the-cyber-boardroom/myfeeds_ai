from typing                                                                                 import List
from mgraph_db.mgraph.actions.MGraph__Screenshot                                            import ENV_NAME__URL__MGRAPH_DB_SERVERLESS
from mgraph_db.providers.time_chain.MGraph__Time_Chain                                      import MGraph__Time_Chain
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Edge                import Schema__MGraph__Time_Chain__Edge__Day, Schema__MGraph__Time_Chain__Edge__Hour, Schema__MGraph__Time_Chain__Edge__Source, Schema__MGraph__Time_Chain__Edge__Month
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types               import Time_Chain__Year, Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File_Extensions
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                     import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB                     import Hacker_News__S3_DB
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article     import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed  import Model__Hacker_News__Data__Feed
from osbot_utils.context_managers.capture_duration                                          import capture_duration
from osbot_utils.helpers.Safe_Id                                                            import Safe_Id
from osbot_utils.helpers.flows.Flow                                                         import Flow
from osbot_utils.helpers.flows.decorators.task                                              import task
from osbot_utils.utils.Env                                                                  import get_env
from osbot_utils.utils.Misc                                                                 import timestamp_to_datetime


FILE__SCREENSHOT__MGRAPH__TIME_SERIES   = './hacker_news-timeline.png'

class Flow__Hacker_News__Create_MGraph__Articles__Timeline(Flow):
    s3_db             : Hacker_News__S3_DB
    files             : Hacker_News__Files
    data_feed         : Model__Hacker_News__Data__Feed      = None
    articles          : List[Model__Hacker_News__Article]   = None
    mgraph_timeseries : MGraph__Time_Chain
    s3_path           : str
    s3_path_latest    : str
    dot_code          : str
    png_bytes         : bytes
    durations                : dict
    duration__load_articles  : float
    duration__create_mgraph  : float
    duration__save_mgraph    : float
    duration__create_dot_code: float
    duration__create_png     : float

    @task()
    def load_articles(self):
        with capture_duration() as duration:
            if not self.data_feed.feed_data.articles:
                raise ValueError("no articles to process")
            self.articles  = self.data_feed.feed_data.articles
            self.log_info(f"loaded {len(self.articles)} articles")
        self.duration__load_articles = duration.seconds

    @task()
    def create_mgraph(self):
        with capture_duration() as duration:
            with self.mgraph_timeseries.create() as _:
                for article in self.articles: # [0:10]:
                    timestamp_utc = article.when.timestamp_utc * 1000
                    date_time     = timestamp_to_datetime(timestamp_utc)
                    _.create_from_datetime(dt=date_time, source_id=article.article_obj_id)
        self.duration__create_mgraph = duration.seconds

    @task()
    def save_mgraph(self):
        with capture_duration() as duration:
            mgraph_json = self.mgraph_timeseries.json__compress()
            with self.s3_db as _:
                self.s3_path        = _.s3_path__timeline__now__mgraph__json()
                self.s3_path_latest = _.s3_path__timeline__latest__mgraph__json()
                s3_key              = _.s3_key__for_provider_path    (self.s3_path)
                s3_key_latest       = _.s3_key__for_provider_path    (self.s3_path_latest)
                result              = _.s3_save_data                 (data=mgraph_json, s3_key=s3_key       )
                result_latest       = _.s3_save_data                 (data=mgraph_json, s3_key=s3_key_latest)
                if result and result_latest:
                    self.log_info("Timeseries MGraph saved ok")

        self.duration__save_mgraph = duration.seconds
        #json_file_create(path=FILE__DATA__MGRAPH__TIMELINE, python_object=mgraph_json)
        #pprint(file_size(FILE__DATA__MGRAPH__TIMELINE))
        # scheme_name = MGraph__Export__Dot__Time_Series__Colors__Scheme.SUNSET
        # MGraph__Export__Dot__Time_Series__Colors(dot_export=_).apply_color_scheme(scheme_name=scheme_name)

    def save_to_s3__now_and_latest(self, data: dict, file_id:Safe_Id, extension: S3_Key__File_Extensions):
        pass

    @task()
    def create_dot_code(self):                          # todo: there is a weird performance issue which only happens on an lambda where this takes about 5 secs to complete (for 50 articles)
        with capture_duration() as duration:
            year_color   = '#E6EEF8'      # Light steel blue
            month_color  = '#D1E2F4'      # Lighter powder blue
            day_color    = '#B3D1F8'      # Soft sky blue
            hour_color   = '#93C4F5'      # Light cerulean
            source_color = '#CCE5FF'      # Very light blue

            link_color_month = '#2C5282'   # Deep blue
            link_color_day = '#3B4B89'     # Navy blue
            link_color_hour = '#4A5491'    # Dark slate blue
            link_color_source = '#5A5C98'  # Dark purple blue
            screenshot = self.mgraph_timeseries.screenshot()
            # _.set_graph__rank_dir__lr()
            # _.set_graph__layout_engine__fdp()
            #_.set_graph__layout_engine__neato()
            # _.set_graph__layout_engine__circo()
            # _.set_graph__epsilon          (0.1)
            # _.set_node__font__size           (30 )      # was 12
            # _.set_graph__title("50 THN Articles published dates")
            with screenshot.export().export_dot() as _:
                _.show_edge__type                ()
                _.show_node__value               ()
                _.set_graph__rank_dir__tb        ()
                _.set_graph__rank_sep            (0.2)
                _.set_graph__node_sep            (0.1)
                _.set_node__shape__type__box     (   )
                _.set_node__shape__rounded       (   )

                _.set_edge__font__size           (7 )      # was 7
                _.set_edge__arrow_head__normal   (   )
                _.set_edge__arrow_size           (0.5)
                _.set_value_type_fill_color      (Time_Chain__Year  , year_color  )
                _.set_value_type_fill_color      (Time_Chain__Month , month_color )
                _.set_value_type_fill_color      (Time_Chain__Day   , day_color   )
                _.set_value_type_fill_color      (Time_Chain__Hour  , hour_color  )
                _.set_value_type_fill_color      (Time_Chain__Source, source_color)
                _.set_value_type_rounded         (Time_Chain__Year                )
                _.set_value_type_rounded         (Time_Chain__Month               )
                _.set_value_type_rounded         (Time_Chain__Hour                )
                _.set_value_type_rounded         (Time_Chain__Source              )
                _.set_value_type_font_size       (Time_Chain__Hour  , 7           )
                _.set_value_type_size            (Time_Chain__Hour  , 0.2         )
                _.set_value_type_font_size       (Time_Chain__Source, 1           )
                _.set_value_type_shape           (Time_Chain__Source, 'point'     )
                _.set_value_type_size            (Time_Chain__Source, 0.1         )

                _.set_value_type_shape     (Time_Chain__Day   , 'diamond' )
                _.set_edge__type_color(Schema__MGraph__Time_Chain__Edge__Month  , link_color_month  )
                _.set_edge__type_color(Schema__MGraph__Time_Chain__Edge__Day    , link_color_day    )
                _.set_edge__type_color(Schema__MGraph__Time_Chain__Edge__Hour   , link_color_hour   )
                _.set_edge__type_color(Schema__MGraph__Time_Chain__Edge__Source , link_color_source )

            self.dot_code = screenshot.export().to__dot()
        self.duration__create_dot_code = duration.seconds
    @task()
    def create_png(self):
        with capture_duration() as duration:
            with self.mgraph_timeseries.screenshot() as _:
                if get_env(ENV_NAME__URL__MGRAPH_DB_SERVERLESS):
                    self.png_bytes = _.dot_to_png(self.dot_code)
        self.duration__create_dot_code = duration.seconds
        # with screenshot as _:
        #     #_.save_to(FILE__SCREENSHOT__MGRAPH__TIME_SERIES)
        #     #_.export().export_dot().show_node__value()
        #     self.dot_code = _.export().to__dot()
        #     self.png_bytes = _.dot_to_png(self.dot_code)
        #     print(len(self.dot_code ))
        #     print(len(self.png_bytes))
        #     #_.dot(print_dot_code=False)

    @task()
    def map_durations(self):
        self.durations = dict(  load_articles   = self.duration__load_articles   ,
                                create_mgraph   = self.duration__create_mgraph   ,
                                save_mgraph     = self.duration__save_mgraph     ,
                                create_dot_code = self.duration__create_dot_code ,
                                create_png      = self.duration__create_png      )

    #@type_safe
    def main(self, data_feed: Model__Hacker_News__Data__Feed):
        self.data_feed = data_feed
        self.load_articles           ()
        self.create_mgraph           ()
        self.save_mgraph             ()
        self.create_dot_code         ()
        self.create_png              ()
        self.map_durations           ()
