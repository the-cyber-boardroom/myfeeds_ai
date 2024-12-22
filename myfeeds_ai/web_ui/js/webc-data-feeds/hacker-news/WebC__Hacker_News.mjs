import { Div, H, A, Raw_Html, Web_Component,
         CSS__Cards, CSS__Typography }            from './../WebC.mjs'

// Helper class for header section
class Header__Component {
    constructor(container) {
        this.container = container
    }

    news_icon_svg() {
        return `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
                     class="lucide lucide-newspaper w-8 h-8 text-blue-600">
                    <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"></path>
                    <path d="M18 14h-8"></path><path d="M15 18h-5"></path>
                    <path d="M10 6h8v4h-8V6Z"></path>
                </svg>`
    }

    render() {
        const header = new Div({ class: 'feed-header' })
        const header_left = new Div({ class: 'header-left' }).add_elements(
            new Raw_Html({ class: 'feed-icon', value: this.news_icon_svg() }),
            new H  ({ level: 1, class: 'feed-title', value: 'Hacker News Feed' })
        )

        const header_links = new Div({ class: 'header-links' }).add_elements(
            new A({ class: 'nav-link', href: 'https://thehackernews.com/'  , value: 'Visit Hacker News'   , target: '_blank' }),
            new A({ class: 'nav-link', href: 'https://dev.myfeeds.ai/docs' , value: 'API Documentation'   , target: '_blank' })
        )

        const logo = new A({ href: 'https://thecyberboardroom.com' }).add_element(
            new Div({ tag: 'img',
                     class: 'cbr-logo',
                     src: 'https://static.dev.aws.cyber-boardroom.com/cbr-static/latest/assets/cbr/cbr-logo-beta.png',
                     alt: 'Cyber Boardroom Logo' })
        )

        header.add_elements(header_left, header_links, logo)
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
            ".feed-container"     : { padding          : "2rem"                      ,         // Main container
                                    maxWidth          : "1200px"                     ,
                                    margin           : "0 auto"                      },

            ".feed-header"        : { display          : "flex"                      ,         // Header section
                                    justifyContent   : "space-between"              ,
                                    alignItems       : "center"                     ,
                                    marginBottom     : "2rem"                       },

            ".header-left"        : { display          : "flex"                      ,         // Left header content
                                    alignItems       : "center"                     ,
                                    gap             : "1rem"                        },

            ".header-links"       : { display          : "flex"                      ,         // Header links
                                    gap              : "2rem"                        },

            ".nav-link"           : { color            : "#4285f4"                   ,         // Navigation links
                                    textDecoration   : "none"                       ,
                                    display         : "flex"                        ,
                                    alignItems      : "center"                      ,
                                    gap             : "0.5rem"                      },

            ".articles-area"      : { backgroundColor : "#f8f9fa"                    ,         // Articles container
                                    borderRadius     : "0.5rem"                      ,
                                    padding         : "2rem"                         },

            ".article-card"       : { backgroundColor : "#ffffff"                    ,         // Article cards
                                    borderRadius     : "0.5rem"                      ,
                                    padding         : "1.5rem"                       ,
                                    marginBottom    : "1rem"                         ,
                                    boxShadow       : "0 2px 4px rgba(0,0,0,0.05)"  },

            ".article-title"      : { fontSize         : "1.25rem"                   ,         // Article title
                                    fontWeight       : "500"                         ,
                                    marginBottom     : "0.75rem"                     },

            ".article-meta"       : { display          : "flex"                      ,         // Article metadata
                                    gap              : "1rem"                        ,
                                    color           : "#666666"                      ,
                                    marginBottom    : "1rem"                         },

            ".read-more"          : { color            : "#4285f4"                   ,         // Read more link
                                    textDecoration   : "none"                        },

            ".cbr-logo"           : { height           : "5.5rem"                    ,         // Logo styling
                                      marginLeft       : "auto"                        }
        }
    }
}

// Main web component class
export default class WebC__Hacker_News extends Web_Component {

    url__data_feed_current = 'https://dev.myfeeds.ai/public-data/hacker-news/latest/feed-data.json'
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

        // Add header component
        const header = new Header__Component(this)
        container.add_element(header.render())

        // Add articles component
        const articles = new Articles__Component(this.articles)
        container.add_element(articles.render())

        return container
    }

    async fetch_url(url) {
        return await fetch(url)
    }
}

WebC__Hacker_News.define()