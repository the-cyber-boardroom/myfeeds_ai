import Tag  from  './Tag.mjs'
import Text from './Text.mjs'

export default class Div extends Tag {
    constructor({...kwargs}={}) {
        super({tag:'div',...kwargs})
    }
    add_div({...kwargs}={}) {
        const div = new Div({...kwargs})
        this.add_element(div)
        return div
    }
    add_tag({...kwargs}={}) {
        const tag = new Tag({...kwargs})
        this.add_element(tag)
        return tag
    }

    add_text(value) {
        const text = new Text({value:value})
        this.add_element(text)
        return text
    }
}