import Tag from "./Tag.mjs";

export default class B extends Tag {
    constructor({...kwargs} = {}) {
        super({tag: 'p', ...kwargs})
    }
}