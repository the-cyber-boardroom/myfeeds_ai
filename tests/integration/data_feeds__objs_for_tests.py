from osbot_local_stack.local_stack.Local_Stack           import Local_Stack
from osbot_aws.testing.Temp__Random__AWS_Credentials     import Temp_AWS_Credentials
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from osbot_utils.utils.Env                               import set_env

DATA_FEEDS__TEST__AWS_ACCOUNT_ID = '000011110000'
DATA_FEEDS__REQUEST_CACHE__FILE  = '/tmp/requests-cache-news-feed.sqlite'

def setup_local_stack() -> Local_Stack:                          # todo: refactor this to the OSBot_Local_Stack code base
    Temp_AWS_Credentials().set_vars()
    set_env('AWS_ACCOUNT_ID', DATA_FEEDS__TEST__AWS_ACCOUNT_ID)  # todo: fix the Temp_AWS_Credentials so that we don't need use this set_env
    local_stack = Local_Stack().activate()
    return local_stack

def setup_requests_cache():
    import requests_cache
    requests_cache.install_cache(DATA_FEEDS__REQUEST_CACHE__FILE)
    # todo: add better support for removing cache entries from the cache, which is done by adding "expire_after=0" to the request.get

class Myfeeds__Test_Data(Type_Safe):
    data_feeds__local_stack      = None
    data_feeds__fast_api         = None
    data_feeds__fast_api__app    = None
    data_feeds__fast_api__client = None
    api__not_setup               : bool = True
    localstack__not_setup        : bool = True

myfeeds_test_data = Myfeeds__Test_Data()

def myfeeds_tests__setup_fast_api__and_localstack():

    if myfeeds_test_data.api__not_setup:
        myfeeds_tests__setup_local_stack()
        from myfeeds_ai.fast_api.Data_Feeds__Fast_API            import Data_Feeds__Fast_API
        with myfeeds_test_data as _:
            _.data_feeds__fast_api         = Data_Feeds__Fast_API().setup()
            _.data_feeds__fast_api__app    = _.data_feeds__fast_api.app()
            _.data_feeds__fast_api__client = _.data_feeds__fast_api.client()
    return myfeeds_test_data

#setup_requests_cache()

def myfeeds_tests__setup_local_stack():
    #global data_feeds__local_stack
    if myfeeds_test_data.localstack__not_setup:
        with myfeeds_test_data as _:
            _.data_feeds__local_stack      = setup_local_stack()
            assert _.data_feeds__local_stack.check__local_stack__health() is True