import Events__Dispatch    from "./Events__Dispatch.mjs";
import Events__Receive     from "./Events__Receive.mjs";

export default class Events__Utils {

    constructor() {
        this.events_dispatch = new Events__Dispatch()
        this.events_receive  = new Events__Receive()
    }

    raise_event() {
        //console.log('raising event.......')
    }



}