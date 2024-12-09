import requests_cache
from osbot_local_stack.local_stack.Local_Stack           import Local_Stack
from cbr_custom_data_feeds.fast_api.Data_Feeds__Fast_API import Data_Feeds__Fast_API
from osbot_aws.testing.Temp__Random__AWS_Credentials     import Temp_AWS_Credentials
from osbot_utils.utils.Env                               import set_env

NEWS_FEEDS__TEST__AWS_ACCOUNT_ID = '000011110000'
NEWS_FEEDS__REQUEST_CACHE__FILE  = '/tmp/requests-cache-news-feed.sqlite'

def setup_local_stack() -> Local_Stack:                          # todo: refator this to the OSBot_Local_Stack code base
    Temp_AWS_Credentials().set_vars()
    set_env('AWS_ACCOUNT_ID', NEWS_FEEDS__TEST__AWS_ACCOUNT_ID)  # todo: fix the Temp_AWS_Credentials so that we don't need use this set_env
    local_stack = Local_Stack().activate()
    return local_stack

def setup_requests_cache():
    requests_cache.install_cache(NEWS_FEEDS__REQUEST_CACHE__FILE)
    # todo: add better support for removing cache entries from the cache, which is done by adding "expire_after=0" to the request.get

data_feeds__local_stack      = setup_local_stack()
data_feeds__fast_api         = Data_Feeds__Fast_API().setup()
data_feeds__fast_api__app    = data_feeds__fast_api.app()
data_feeds__fast_api__client = data_feeds__fast_api.client()

setup_requests_cache()

def cbr_website__assert_local_stack():
    assert data_feeds__local_stack.is_local_stack_configured_and_available() is True