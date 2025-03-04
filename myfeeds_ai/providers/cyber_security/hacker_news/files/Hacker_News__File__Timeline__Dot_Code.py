from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import FILE_ID__TIMELINE__MGRAPH
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File    import Hacker_News__File
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Edge    import Schema__MGraph__Time_Chain__Edge__Day, Schema__MGraph__Time_Chain__Edge__Hour, Schema__MGraph__Time_Chain__Edge__Source, Schema__MGraph__Time_Chain__Edge__Month
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types   import Time_Chain__Year, Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source
from osbot_utils.utils.Misc                                                     import bytes_to_str

year_color        = '#E6EEF8'       # Light steel blue
month_color       = '#D1E2F4'       # Lighter powder blue
day_color         = '#B3D1F8'       # Soft sky blue
hour_color        = '#93C4F5'       # Light cerulean
source_color      = '#CCE5FF'       # Very light blue

link_color_month  = '#2C5282'       # Deep blue
link_color_day    = '#3B4B89'       # Navy blue
link_color_hour   = '#4A5491'       # Dark slate blue
link_color_source = '#5A5C98'       # Dark purple blue

CONTENT_TYPE__MGRAPH__DOT = "text/vnd.graphviz"

class Hacker_News__File__Timeline__Dot_Code(Hacker_News__File):
    file_id      = FILE_ID__TIMELINE__MGRAPH
    extension    = S3_Key__File_Extension.MGRAPH__DOT
    content_type = CONTENT_TYPE__MGRAPH__DOT

    def create_dot_code(self, mgraph_timeline):

        screenshot = mgraph_timeline.screenshot()

        with screenshot.export().export_dot() as _:
            _.show_edge__type__str           ()
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

        return screenshot.export().to__dot()

    def load(self):
        file_bytes = super().load()            # because content_type is set, the data is stored as bytes
        return bytes_to_str(file_bytes)     # so we need to convert it back into an str