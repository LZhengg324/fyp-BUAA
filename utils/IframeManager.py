from typing import Callable, Optional, List

from trame.widgets import client
from trame_iframe.widgets.iframe import Communicator
from trame_server import Server

class IframeManager:
    def __init__(self, server: Server):
        self.server: Server = server
        self.server.controller.trigger_name("post_message_to_parent")
        self.event_map: dict[str, (Callable[[str], None], str)] = {}
        self.communicator: Optional[Communicator] = None

    def add_event(self, event_name: str, func: Callable[[str], None]):
        self.event_map[event_name] = (func, "[$event]")

    def register(self):
        event_names: List[str] = []
        event_funcs: List[Callable[[str], None]] = []
        for event_name, event_func in self.event_map.items():
            event_names.append(event_name)
            event_funcs.append(event_func)
        self.communicator = Communicator(
            event_names=event_names,
            **self.event_map
        )

        self.server.controller.post_message_to_parent = client.JSEval(
            exec="window.parent.postMessage({emit: $event.emit, value: $event.value}, '*');").exec
        @self.server.controller.trigger("post_message_to_parent")
        def post_message_to_parent_trigger(message_event: dict[str, str]):
            self.post_message_to_parent(message_event)

    def post_message_to_parent(self, message_event: dict[str, str]) -> None:
        """
        向父界面发送消息
        :param message_event: {"emit": emit, "value": value}
        :return:
        """
        self.server.controller.post_message_to_parent(message_event)

