from mangum                                              import Mangum
from osbot_utils.utils.Env                               import get_env
from myfeeds_ai.fast_api.Data_Feeds__Fast_API import Data_Feeds__Fast_API

fast_api__data_feeds = Data_Feeds__Fast_API().setup()
app                  = fast_api__data_feeds.app()
run                  = Mangum(app)

if __name__ == "__main__":                              # pragma: no cover
    import uvicorn
    port = get_env('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=port)