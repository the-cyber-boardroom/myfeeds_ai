from enum import Enum

class Schema__Feed__Article__Step(Enum):
    STEP__1__SAVE_ARTICLE          : str = 'step-1-save-article'
    STEP__2__MARKDOWN__FOR_ARTICLE : str = 'step-2-markdown-for-article'
    STEP__3__LLM__TEXT_TO_GRAPH    : str = 'step-3-text-to-graph'
    STEP__4__CREATE_GRAPH          : str = 'step-4-create-graph'
    STEP__5__MERGE_GRAPH           : str = 'step-5-merge-graph'