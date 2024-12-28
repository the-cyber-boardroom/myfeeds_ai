import { Div, H, A, Raw_Html, Web_Component,
         CSS__Cards, CSS__Typography }            from './../WebC.mjs'

// Main web component class
export default class WebC__Hacker_News extends Web_Component {
    server__data         = 'https://dev.myfeeds.ai'
    server__static       = 'https://static.dev.aws.cyber-boardroom.com/cbr-static/latest'
    // server__data           = 'http://localhost:7777'
    // server__static         = '/static'
    url__data_feed_current = `${this.server__data}/public-data/hacker-news/latest/feed-data.json`
    url__cbr_logo          = `${this.server__static}/assets/cbr/cbr-logo-beta.png`
    url__hacker_news_com   = 'https://thehackernews.com/'
    url__api_documentation = '/docs'
    data_feed              = null
    feed_data              = null
    articles               = null

    apply_css() {
        new CSS__Cards     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        this.add_css_rules(CSS__Rules.get_rules())
    }

    async load_data() {
        const response = await this.fetch_url(this.url__data_feed_current)
        if (response.status === 200) {
            this.data_feed = await response.json()
            this.feed_data = this.data_feed.feed_data
            this.articles  = this.feed_data.articles
        }
    }

    html() {
        const container = new Div({ class: 'feed-container' })

        const header = new Header__Component(this)                      // Add header component
        const articles = new Articles__Component(this.articles)         // Add articles component

        container.add_element(header.render  ())
        container.add_element(articles.render())

        return container
    }

    async fetch_url(url) {
        return await fetch(url)
    }

    get feed_title       () { return this.feed_data.title                      }
    get feed_description () { return this.feed_data.description                }
    get dom_title        () { return  this.query_selector('.feed-title'      ) }
    get dom_description  () { return  this.query_selector('.feed-description') }
}

// Helper class for header section
class Header__Component {

    constructor(container) {
        this.container = container
    }

    news_icon_svg() {
        return `<svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 24 24" fill="none" 
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
                     class="news-icon">
                    <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"></path>
                    <path d="M18 14h-8"></path><path d="M15 18h-5"></path>
                    <path d="M10 6h8v4h-8V6Z"></path>
                </svg>`
    }

    render() {

        const header         = new Div     ({ class: 'feed-header'                                               })
        const header_content = new Div     ({ class: 'header-content'                                            })
        const feed_icon      = new Raw_Html({ class: 'feed-icon'        , value: this.news_icon_svg()            })
        const feed_title     = new Div     ({ class: 'feed-title'       , value: this.container.feed_title       })
        const header_left    = new Div     ({ class: 'header-left'                                               })
        const description    = new Div     ({ class: 'feed-description' , value: this.container.feed_description })
        const header_links   = new Div     ({ class: 'header-links'                                              })
        const link_visit_hn  = new A       ({ class: 'nav-link'         , value: 'Visit Hacker News' , href: this.container.url__hacker_news_com   , target: '_blank' })
        const link_api_docs  = new A       ({ class: 'nav-link'         , value: 'API Documentation' , href: this.container.url__api_documentation , target: '_blank' })

        const powered_by     = new Div    ({ class:'powered-by', value:"powered by"})
        const cbr_logo       = new Div    ({ class: 'cbr-logo',  tag: 'img',  src: this.container.url__cbr_logo,  alt: 'Cyber Boardroom Logo' })
        const cbr_link       = new A      ({ href: 'https://thecyberboardroom.com' , target:'_blank' })
        const header_logo    = new Div    ({ class: 'header-logo' })

        header_left   .add_elements(feed_icon     , feed_title               )
        header_links  .add_elements(link_visit_hn , link_api_docs            )
        cbr_link      .add_elements(cbr_logo)
        header_logo   .add_elements(powered_by, cbr_link)
        header_content.add_elements(header_left   , description, header_links)
        header        .add_elements(header_content, header_logo              )
        return header
    }
}

// Helper class for articles section
class Articles__Component {
    constructor(articles) {
        this.articles = articles
    }

    render_article(article) {
        return new Div({ class: 'article-card' }).add_elements(
            new H({ level: 2, class: 'article-title', value: article.title }),
            new Div({ class: 'article-meta' }).add_elements(
                new Div({ value: article.author || 'Unknown' }),
                new Div({ value: article.date || 'Invalid Date' })
            ),
            new A({ class: 'read-more', href: article.url || '#', value: 'Read More →', target: '_blank' })
        )
    }

    render() {
        const articles_area = new Div({ class: 'articles-area' })

        if (this.articles) {
            this.articles.forEach(article => {
                articles_area.add_element(this.render_article(article))
            })
        }

        return articles_area
    }
}

// Helper class for CSS rules
class CSS__Rules {
    static get_rules() {
        return {
            ".feed-container"   : { padding          : "2rem"                       ,         // Main container
                                    maxWidth          : "1200px"                    ,
                                    margin           : "0 auto"                     },
            ".header-content"   : { display          : "flex"                       ,
                                    flexDirection    : "column"                     },
            ".feed-header"      : { display          : "flex"                       ,         // Header section
                                    justifyContent   : "space-between"              ,
                                    alignItems       : "center"                     ,
                                    padding          : "20px"                       },

            ".header-left"      : { display          : "flex"                       ,         // Left header content
                                    alignItems       : "center"                     ,
                                    gap              : "1rem"                       },

            ".header-links"     : { display          : "flex"                      ,         // Header links
                                    gap              : "2rem"                        },

            ".nav-link"         : { color            : "#4285f4"                   ,         // Navigation links
                                    textDecoration   : "none"                       ,
                                    display          : "flex"                        ,
                                    alignItems       : "center"                      ,
                                    gap              : "0.5rem"                      },
            ".feed-title"       : { fontSize         : "2.0rem"                      },
            ".articles-area"    : { backgroundColor: "#f8f9fa"                    ,         // Articles container
                                    borderRadius     : "0.5rem"                      ,
                                    padding         : "2rem"                         },

            ".article-card"     : { backgroundColor : "#ffffff"                    ,         // Article cards
                                    borderRadius     : "0.5rem"                      ,
                                    padding         : "1.5rem"                       ,
                                    marginBottom    : "1rem"                         ,
                                    boxShadow       : "0 2px 4px rgba(0,0,0,0.05)"  },

            ".article-title"    : { fontSize         : "1.25rem"                   ,         // Article title
                                    fontWeight       : "500"                         ,
                                    marginBottom     : "0.75rem"                     },

            ".article-meta"       : { display          : "flex"                      ,         // Article metadata
                                    gap              : "1rem"                        ,
                                    color           : "#666666"                      ,
                                    marginBottom    : "1rem"                         },

            ".read-more"          : { color            : "#4285f4"                   ,         // Read more link
                                    textDecoration   : "none"                        },

            ".cbr-logo"           : { height           : "5.5rem"                    ,         // Logo styling
                                      marginLeft       : "auto"                      },
            ".news-icon"          : { color            : "rgb(37 99 235)"            },
            ".powered-by"         : { textAlign        : "center"                    },
            ".feed-description"   : { padding          : "20px"                      ,
                                      fontStyle        : "italic"                     }

        }
    }
}


WebC__Hacker_News.define()