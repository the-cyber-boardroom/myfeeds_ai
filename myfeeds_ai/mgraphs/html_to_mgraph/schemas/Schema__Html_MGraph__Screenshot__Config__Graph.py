from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Layout__Engine import MGraph__Export__Dot__Layout__Engine
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe


class Schema__Html_MGraph__Screenshot__Config__Graph(Type_Safe):
    """Graph-wide configuration settings"""
    title           : str = "HTML MGraph"
    title_font_size : int = 30
    title_font_color: str = "#333333"
    bg_color        : str = "#f8f9fa"
    rank_sep        : float = 1.0           # vertical separation distance
    node_sep        : float = 0.8           # distance between nodes
    margin          : float = 0.2           # graph margin
    layout_engine   : MGraph__Export__Dot__Layout__Engine = None
    spring_constant : float = None          # string strength in FDP