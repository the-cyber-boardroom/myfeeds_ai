import Tag from './Tag.mjs'

export default class H extends Tag {
    constructor({level=1, value='', ...kwargs}={}) {
        const tag = `h${level}`
        super({tag: tag, ...kwargs});
        this.value = value
        this.config()
    }

    add_element(element) {              // add elements not allowed
        return false
    }
    config() {
        this.html_config.new_line_before_elements = false
        this.html_config.indent_before_last_tag   = false
    }
    inner_html() {
        return this.value
    }

}