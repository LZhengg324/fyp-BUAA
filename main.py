import os.path

from trame.app import get_server
from trame.decorators import controller
from trame_client.widgets.html import Div, Iframe
from trame_server import Server
from trame_server.controller import Controller
from trame_server.state import State
from trame.widgets import vuetify3 as vuetify
from trame_vuetify.ui.vuetify3 import SinglePageLayout

from utils.IframeManager import IframeManager

server: Server = get_server()
state: State = server.state
state.received_messages = []
state.file_content = ""

def received_messages(message: str) -> None:
    print(message)
    state.received_messages += [message]
    state.dirty("received_messages")

def read_file(file_name: str) -> None:
    file_path = os.path.join("/data", file_name)
    print(file_path)
    with open(file_path, "r") as file:
        content = file.read()
        state.file_content = content
        state.dirty("file_content")

iframe_manager: IframeManager = IframeManager(server)
iframe_manager.add_event("post_message_to_iframe", received_messages)
iframe_manager.add_event("post_file_name_to_iframe", read_file)

with SinglePageLayout(server) as layout:
    iframe_manager.register()
    with layout.content:
        with vuetify.VContainer():
            with vuetify.VCard():
                vuetify.VCardTitle("Iframe Post Message To Parent")
                with vuetify.VCardText():
                    vuetify.VBtn("Post Message To Parent", click=(
                        iframe_manager.post_message_to_parent,
                        "[{emit: 'From Iframe', value: 'Hello World'}]"
                    ))

            with vuetify.VCard():
                vuetify.VCardTitle("Iframe Received Messages From Parent")
                with vuetify.VCardText():
                    Div("No Message Received From Parent", v_if="received_messages.length === 0")
                    Div("{{ messsage }}", v_for="messsage, index of received_messages", key="index")

            with vuetify.VCard():
                vuetify.VCardTitle("Iframe Read File Content")
                vuetify.VCardText("{{file_content}}")

server.start(port=9000)