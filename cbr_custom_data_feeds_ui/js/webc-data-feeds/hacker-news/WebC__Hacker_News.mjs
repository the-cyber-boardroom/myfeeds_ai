
import { Div,H, P, Web_Component,
         CSS__Cards, CSS__Typography }            from './../WebC.mjs'


export default class WebC__Hacker_News extends Web_Component {

    url__data_feed_current = 'https://data-feeds.dev.aws.cyber-boardroom.com/public-data/hacker-news/latest/feed-data.json'
    data_feed              = null
    feed_data              = null
    articles               = null

    apply_css() {
        new CSS__Cards     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
    }
    async load_data () {
        const  response = await this.fetch_url(this.url__data_feed_current)
        if (response.status === 200) {
            this.data_feed = await  response.json()
            this.feed_data = this.data_feed.feed_data
            this.articles  = this.feed_data.articles
        }
    }

    async fetch_url(url) {
        return await fetch(url)
    }

    html() {
        const div_root = new Div()
        const h1_title = new H({level:2, value: this.feed_data.title})

        const card = new Div({ class: 'card bg-secundary color-white'}).add_elements(
                new Div({ class: 'card-header', value: 'Header' }),
                new Div({ class: 'card-body' }).add_elements(
                    new Div({ class: 'card-title', value: 'Primary card title' }),
                    new P({ class: 'card-text', value: 'Some quick example text to build on the card title and make up the bulk of the card\'s content.' })
                )
            )

        div_root.add_elements(h1_title, card)
        return div_root
    }

    get title() {
        return this.query_selector('h2')
    }
}

WebC__Hacker_News.define()