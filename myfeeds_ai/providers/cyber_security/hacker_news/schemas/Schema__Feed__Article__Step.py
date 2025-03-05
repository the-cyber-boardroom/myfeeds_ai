from enum import Enum

class Schema__Feed__Article__Step(Enum):
    STEP__1__SAVE_ARTICLE       : str = 'step-1-save-article'
    STEP__2__LLM__TEXT_TO_GRAPH : str = 'step-2-text-to-graph'
    STEP__3__CREATE_GRAPH       : str = 'step-3-create-graph'
    STEP__4__MERGE_GRAPH        : str = 'step-4-merge-graph'