//import WebC__Hacker_News from "../../../../cbr_custom_data_feeds/web_ui/js/webc-data-feeds/hacker-news/WebC__Hacker_News.mjs";
const { module, test , only} = QUnit

module('WebC__Hacker_News', (hooks)=>{

    let host_div, webc_simple_test

    test('find dependency', async (assert)=>{
        console.log('123a')
        const result = await fetch('../../..//cbr_custom_data_feeds/web_ui/js/webc-data-feeds/hacker-news/WebC__Hacker_News.mjs')
        console.log(result.status)
        assert.ok(1)
    })
    // hooks.before(async (assert)=> {
    //     const timeout= 500
    //     assert.timeout(timeout)
    //     host_div = document.createElement('div')
    //     document.body.appendChild(host_div)
    //     webc_simple_test = host_div.appendChild(WebC__Hacker_News.create())
    //     await webc_simple_test.wait_for__component_ready(timeout)
    // })
    //
    // hooks.after(async ()=> {
    //     webc_simple_test.remove()
    //     host_div.remove()
    // })
    //
    // only('ctor', async (assert) => {
    //     const feed_data = webc_simple_test.feed_data
    //     const articles =  webc_simple_test.articles
    //     assert.equal(feed_data.title, 'The Hacker News')
    //     assert.equal(articles.length , 50              )
    // })
    //
    // test('html', async (assert) => {
    //     const h2_title = webc_simple_test.title
    //     assert.equal(h2_title.innerHTML, 'The Hacker News')
    // })
})