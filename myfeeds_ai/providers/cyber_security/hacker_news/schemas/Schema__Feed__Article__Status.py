from enum import Enum

class Schema__Feed__Article__Status(Enum):
    TO_PROCESS                  : str = 'process'
    PROCESSING                  : str = 'processing'
    PROCESSED                   : str = 'processed'
    ERROR__NO_FEED_DATA         : str = 'error-no-feed-data'
    ERROR__FAILED_TASK          : str = 'error-failed-task'
