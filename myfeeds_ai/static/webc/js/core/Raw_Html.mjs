import Tag from './Tag.mjs'

export default class Raw_Html extends Tag {
    constructor({value='', ...kwargs}={}) {
        super({tag: 'div', ...kwargs});
        this.raw_html = value || ''
        this.config()
    }

    add_element(element) {              // html elements should NOT have any child elements
        return false                    // return false to indicate that the element was not added
    }
    config() {
        //this.html_config.include_tag          = false
        //this.html_config.trim_final_html_code = false
        return this
    }

    inner_html(depth) { // todo: need to add support for indent in inner_html

        if (typeof this.raw_html !== 'string' || this.raw_html.trim() === '') {                         // Ensure raw_html is a string and handle null or empty cases
            return '';
        } else {
            const indent = ' '.repeat((depth + 1) * 4);
            const indentedHtml = this.raw_html.split('\n')                                              // Split the raw HTML into lines
                                              .map(line => indent + line)                        // Add the indent to each line
                                              .join('\n');                                              // Join them back with newlines
            return indentedHtml + '\n';                                                                 // Ensure the result ends with a newline for better formatting
        }
    }

}