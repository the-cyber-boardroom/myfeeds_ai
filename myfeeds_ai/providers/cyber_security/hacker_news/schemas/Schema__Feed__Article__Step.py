from enum import Enum

class Schema__Feed__Article__Step(Enum):
    STEP__1__SAVE__ARTICLE                : str = 'step-1-save-article'
    STEP__2__MARKDOWN__FOR_ARTICLE        : str = 'step-2-markdown-for-article'
    STEP__3__LLM__TEXT_TO_ENTITIES        : str = 'step-3-llm-text-to-entities'
    STEP__4__CREATE__TEXT_ENTITIES_GRAPHS : str = 'step-4-create-text-entities-graphs'
    STEP__5__MERGE__TEXT_ENTITIES_GRAPHS  : str = 'step-5-merge-text-entities-graphs'
    STEP__6__MERGE__DAY_ENTITIES_GRAPHS   : str = 'step-7-merge-day-entities-graphs'
    STEP__7__MERGE__FEED_ENTITIES_GRAPHS  : str = 'step-7-merge-feed-entities-graphs'