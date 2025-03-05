from mgraph_db.providers.time_chain.MGraph__Time_Chain                           import MGraph__Time_Chain
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News  import FILE_ID__TIMELINE__MGRAPH
from myfeeds_ai.providers.cyber_security.hacker_news.mgraphs.Hacker_News__MGraph import Hacker_News__MGraph
from osbot_utils.helpers.Safe_Id                                                 import Safe_Id

class Hacker_News__MGraph__Timeline(Hacker_News__MGraph):
    file_id : Safe_Id            =  FILE_ID__TIMELINE__MGRAPH
    mgraph  : MGraph__Time_Chain
