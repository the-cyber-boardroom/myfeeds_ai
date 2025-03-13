from osbot_utils.helpers.Safe_Id import Safe_Id

S3_BUCKET_PREFIX__DATA_FEEDS        = 'data-feeds'
S3_BUCKET_SUFFIX__HACKER_NEWS       = 'data'

S3_FILE_NAME__CONTENT               = Safe_Id('content'         )
S3_FILE_NAME__LATEST__VERSIONS      = Safe_Id('latest-versions' )
S3_FILE_NAME__RAW__FEED_XML         = Safe_Id('feed-xml'        )
S3_FILE_NAME__RAW__FEED_DATA        = Safe_Id('feed-data'       )
S3_FILE_NAME__RAW__CONTENT          = Safe_Id('raw-content'     )

S3_FOLDER_NAME__ARTICLES            = 'articles'
S3_FOLDER_NAME__LATEST              = 'latest'

S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA = 'public-data'