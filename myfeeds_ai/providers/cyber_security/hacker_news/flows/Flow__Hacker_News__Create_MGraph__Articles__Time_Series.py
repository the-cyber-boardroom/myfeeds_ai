from datetime                                                                               import datetime
from typing                                                                                 import List
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value                                   import Schema__MGraph__Node__Value
from mgraph_db.providers.time_chain.MGraph__Time_Chain import MGraph__Time_Chain
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Edge import \
    Schema__MGraph__Time_Chain__Edge__Day, Schema__MGraph__Time_Chain__Edge__Hour, \
    Schema__MGraph__Time_Chain__Edge__Source, Schema__MGraph__Time_Chain__Edge__Month
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types import Time_Chain__Year, \
    Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges             import Schema__MGraph__Time_Series__Edge__Day,Schema__MGraph__Time_Series__Edge__Hour
from mgraph_db.providers.time_series.MGraph__Time_Series                                    import MGraph__Time_Series
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Time_Point               import Schema__MGraph__Node__Time_Point
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                     import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article     import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed  import Model__Hacker_News__Data__Feed
from osbot_utils.context_managers.print_duration import print_duration
from osbot_utils.helpers.flows.Flow                                                         import Flow
from osbot_utils.helpers.flows.decorators.task                                              import task
from osbot_utils.utils.Dev                                                                  import pprint
from osbot_utils.utils.Files                                                                import file_create, file_size
from osbot_utils.utils.Json                                                                 import json_file_create
from osbot_utils.utils.Misc                                                                 import wait_for, timestamp_to_datetime

FILE__DATA__MGRAPH__TIME_SERIES         = './hacker_news-timeseries.mgraph.json'
FILE__SCREENSHOT__MGRAPH__TIME_SERIES   = './hacker_news-timeseries.png'

class Flow__Hacker_News__Create_MGraph__Articles__Time_Series(Flow):
    files             : Hacker_News__Files
    data_feed         : Model__Hacker_News__Data__Feed
    articles          : List[Model__Hacker_News__Article]
    mgraph_time_chain : MGraph__Time_Chain

    @task()
    def load_articles(self):
        self.data_feed = self.files.feed_data__current()
        self.articles  = self.data_feed.feed_data.articles
        print(f"loaded {len(self.articles)} articles")

    def create_mgraph(self):
        with self.mgraph_time_chain.create() as _:
            for article in self.articles[0:150]:
                print(article.when.date_time_utc)
                timestamp_utc = article.when.timestamp_utc * 1000
                date_time     = timestamp_to_datetime(timestamp_utc)
                _.create_from_datetime(dt=date_time, source_id=article.article_obj_id)

        #self.mgraph_timeseries.index().print__stats()

    # def save_mgraph(self):
    #     mgraph_json = self.mgraph_time_chain.json__compress()
    #     json_file_create(path=FILE__DATA__MGRAPH__TIME_SERIES, python_object=mgraph_json)
    #     pprint(file_size(FILE__DATA__MGRAPH__TIME_SERIES))

    # scheme_name = MGraph__Export__Dot__Time_Series__Colors__Scheme.SUNSET
    # MGraph__Export__Dot__Time_Series__Colors(dot_export=_).apply_color_scheme(scheme_name=scheme_name)

    def save_mgraph_screenshot(self):
        year_color   = '#E6EEF8'      # Light steel blue
        month_color  = '#D1E2F4'      # Lighter powder blue
        day_color    = '#B3D1F8'      # Soft sky blue
        hour_color   = '#93C4F5'      # Light cerulean
        source_color = '#CCE5FF'      # Very light blue

        link_color_month = '#2C5282'   # Deep blue
        link_color_day = '#3B4B89'     # Navy blue
        link_color_hour = '#4A5491'    # Dark slate blue
        link_color_source = '#5A5C98'  # Dark purple blue
        screenshot = self.mgraph_time_chain.screenshot()
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
            _.set_graph__rank_dir__lr()
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



        with screenshot as _:
            _.save_to(FILE__SCREENSHOT__MGRAPH__TIME_SERIES)
            #_.export().export_dot().show_node__value()
            _.dot(print_dot_code=True)

    def main(self):
        self.load_articles()
        self.create_mgraph()
        #self.save_mgraph()
        self.save_mgraph_screenshot()
