import Tag from "./Tag.mjs";

export default class A extends Tag {
    constructor({...kwargs} = {}) {
        super({tag: 'a', ...kwargs})
    }
}