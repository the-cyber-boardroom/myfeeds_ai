import datetime
from typing                                             import Dict, Any
from myfeeds_ai.utils.open_observe.Open_Observe__Http   import Open_Observe__Http
from osbot_utils.helpers.flows.actions.Flow__Events     import flow_events
from osbot_utils.helpers.flows.models.Flow_Run__Event   import Flow_Run__Event
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type import Flow_Run__Event_Type
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Flow_Events__To__Open_Observe(Type_Safe):
    open_observe : Open_Observe__Http

    def __enter__(self):
        self.add_event_listener()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_event_listener()
        self.open_observe.session().close()

    def add_event_listener(self):
        flow_events.event_listeners.append(self.event_listener)

    def remove_event_listener(self):
        flow_events.event_listeners.remove(self.event_listener)

    def send_to_openobserve(self, log_entry: Dict[str, Any]):
        log_entry.update({                                                      # Add common fields
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",          # todo: see if we need to add a timestamp
            "source"   : "osbot_utils",
            "log_type" : "flow_event"
        })
        #from osbot_utils.utils.Dev import pprint
        #pprint(log_entry)
        self.open_observe.send_data(log_entry)

    def handle_event(self, flow_event: Flow_Run__Event):
        event_type = flow_event.event_type
        event_data = flow_event.event_data

        # Create base log entry with common fields
        log_entry = { "event_type": event_type.value,
                      "flow_id"   : getattr(event_data, 'flow_id', None),
                      "run_id"    : getattr(event_data, 'run_id', None)}

        # Add event-specific data
        if event_type == Flow_Run__Event_Type.FLOW_MESSAGE:
            log_entry.update({
                "message": getattr(event_data, 'message', None),
                "message_type": getattr(event_data, 'message_type', None)
            })

        elif event_type == Flow_Run__Event_Type.FLOW_START:
            log_entry.update({
                "flow_name": getattr(event_data, 'flow_name', None),
                "parameters": getattr(event_data, 'parameters', None)
            })

        elif event_type == Flow_Run__Event_Type.FLOW_STOP:
            log_entry.update({
                "duration": getattr(event_data, 'duration', None),
                "status": getattr(event_data, 'status', None),
                "error": getattr(event_data, 'error', None)
            })

        elif event_type == Flow_Run__Event_Type.NEW_RESULT:
            log_entry.update({
                "task_id": getattr(event_data, 'task_id', None),
                "result": str(getattr(event_data, 'result', None))[:1000]  # Truncate long results
            })

        elif event_type == Flow_Run__Event_Type.NEW_ARTIFACT:
            log_entry.update({
                "artifact_id": getattr(event_data, 'artifact_id', None),
                "artifact_type": getattr(event_data, 'artifact_type', None)
            })

        elif event_type in [Flow_Run__Event_Type.TASK_START, Flow_Run__Event_Type.TASK_STOP]:
            log_entry.update({ "task_id"  : getattr(event_data, 'task_id', None),
                               "task_name": getattr(event_data, 'task_name', None),
                               "task_type": getattr(event_data, 'task_type', None),
                               "duration" : getattr(event_data, 'duration', None) if event_type == "TASK_STOP" else None })

        else:
            log_entry.update({
                "unknown_event_type": event_type.value,
                #"raw_event_data"    : event_data.json()
            })

        # Send the log entry to OpenObserve
        self.send_to_openobserve(log_entry)

    def event_listener(self, flow_event: Flow_Run__Event):
        self.handle_event(flow_event=flow_event)