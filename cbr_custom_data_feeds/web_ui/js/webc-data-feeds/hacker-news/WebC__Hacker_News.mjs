import { Div, H, P, Web_Component,
         CSS__Cards, CSS__Typography }            from './../WebC.mjs'

export default class WebC__Hacker_News extends Web_Component {

    url__data_feed_current = 'https://data-feeds.dev.aws.cyber-boardroom.com/public-data/hacker-news/latest/feed-data.json'
    data_feed              = null
    feed_data              = null
    articles               = null

    apply_css() {
        new CSS__Cards     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    async load_data() {
        console.log('here', this.url__data_feed_current)
        const response = await this.fetch_url(this.url__data_feed_current)
        console.log('after response')
        if (response.status === 200) {
            this.data_feed = await response.json()
            this.feed_data = this.data_feed.feed_data
            this.articles  = this.feed_data.articles
        }
    }

    html() {
        const container = new Div({ class: 'feed-container' })
        const header    = new Div({ class: 'feed-header'    })

        header.add_elements(
            new Div({ class: 'feed-icon' , value: '📰'                     }),
            new H  ({ level: 1, value   : 'Hacker News Feed'              })
        )

        container.add_element(header)

        if (this.articles) {
            this.articles.forEach(article => {
                const card = new Div({ class: 'article-card' })

                card.add_elements(
                    new Div({ class: 'article-title', value: article.title }),
                    new Div({ class: 'article-meta'  }).add_elements(
                        new Div({ value: `👤 ${article.author || 'Unknown'}` }),
                        new Div({ value: `📅 ${article.date || 'Invalid Date'}` })
                    ),
                    new P({ class: 'read-more', value: 'Read More →' })
                )

                container.add_element(card)
            })
        }

        return container
    }

    async fetch_url(url) {
        return await fetch(url)
    }

    css_rules() {
        return {
            ".feed-container"     : { padding          : "2rem"                      ,         // Main container
                                    maxWidth          : "1200px"                     ,
                                    margin           : "0 auto"                      },

            ".feed-header"        : { display          : "flex"                      ,         // Header section
                                    alignItems        : "center"                     ,
                                    gap              : "1rem"                        ,
                                    marginBottom     : "2rem"                        },

            ".feed-icon"          : { fontSize         : "2rem"                      ,         // Feed icon
                                    color            : "#4285f4"                     },

            ".article-card"       : { backgroundColor : "#ffffff"                    ,         // Article cards
                                    borderRadius     : "0.5rem"                      ,
                                    padding         : "1.5rem"                       ,
                                    marginBottom    : "1rem"                         ,
                                    boxShadow       : "0 2px 4px rgba(0,0,0,0.1)"   },

            ".article-title"      : { fontSize         : "1.25rem"                   ,         // Article title
                                    fontWeight       : "600"                         ,
                                    marginBottom     : "0.5rem"                      ,
                                    color           : "#333333"                      },

            ".article-meta"       : { display          : "flex"                      ,         // Metadata row
                                    gap              : "1rem"                        ,
                                    alignItems       : "center"                      ,
                                    color           : "#666666"                      ,
                                    fontSize        : "0.875rem"                     },

            ".read-more"          : { color           : "#4285f4"                    ,         // Read more link
                                    textDecoration   : "none"                        ,
                                    display         : "inline-flex"                  ,
                                    alignItems      : "center"                       ,
                                    gap             : "0.25rem"                      },

            ".read-more:hover"    : { textDecoration  : "underline"                  }         // Hover effect
        }
    }
}

WebC__Hacker_News.define()