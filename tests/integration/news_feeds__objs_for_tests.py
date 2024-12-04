from cbr_custom_news_feeds.fast_api.News_Feeds__Fast_API import News_Feeds__Fast_API

news_feeds__fast_api         = News_Feeds__Fast_API().setup()
news_feeds__fast_api__app    = news_feeds__fast_api.app()
news_feeds__fast_api__client = news_feeds__fast_api.client()