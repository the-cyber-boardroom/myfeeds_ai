import Tag from  './Tag.mjs'

export default class Text extends Tag {
    constructor({value='', ...kwargs}={}) {
        super({tag:'text', ...kwargs});
        this.value = value
        this.config()
    }

    config() {
        this.html_config.indent_before_last_tag   = false
        this.html_config.new_line_before_elements = false
        this.html_config.new_line_after_final_tag = false
        return this
    }

    add_element(element) {                                          // text elements should NOT have any child elements
        return false                                                // return false to indicate that the element was not added
    }

    inner_html() {
        return this.html_escape(this.value)                         // all data inside the text should html escaped
    }

    just_text() {
        this.html_config.include_tag   = false
        return this
    }
}