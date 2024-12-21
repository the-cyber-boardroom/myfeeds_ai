import WebC__Hacker_News from "../../../../myfeeds_ai/web_ui/js/webc-data-feeds/hacker-news/WebC__Hacker_News.mjs";
const { module, test , only} = QUnit

module('WebC__Hacker_News', (hooks)=>{

    let host_div, webc_hacker_news

    hooks.before(async (assert)=> {
        const timeout= 1500
        assert.timeout(timeout)
        host_div = document.createElement('div')
        document.body.appendChild(host_div)
        webc_hacker_news = host_div.appendChild(WebC__Hacker_News.create())
        await webc_hacker_news.wait_for__component_ready(timeout)
    })

    hooks.after(async ()=> {
        webc_hacker_news.remove()
        host_div.remove()
    })

    test('ctor', async (assert) => {
        const feed_data = webc_hacker_news.feed_data
        const articles =  webc_hacker_news.articles
        assert.equal(feed_data.title, 'The Hacker News')
        assert.equal(articles.length , 50              )
    })

    test('html', async (assert) => {
        const h2_title = webc_hacker_news.title
        assert.equal(h2_title.innerText, 'The Hacker News Feed')
    })

    test('load_data - check url', async (assert) => {
        const url = webc_hacker_news.url__data_feed_current
        assert.equal(url, 'https://dev.myfeeds.ai/public-data/hacker-news/latest/feed-data.json')
        const result = await fetch(url)
        assert.equal(result.status, 200)
        const data = await result.json()
        assert.ok   (data.feed_data)
        assert.ok   (data.feed_data.title)
        assert.equal(data.feed_data.title, 'The Hacker News')

    })
})