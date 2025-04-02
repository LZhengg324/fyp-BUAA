from typing import List, Dict

from trame.widgets import vuetify3 as vuetify, trame
from trame_server import Server

from Components.Drawer.UICardManager.DataHolder import DataHolder
from Constants.card_type import CardType
from Source.SourceManager import SourceManager
from Source.VisibleManager import VisibleManager
from paraview import simple


class PipelineWidget:
    def __init__(self, server: Server, source_manager: SourceManager, visible_manager: VisibleManager, data_holder: DataHolder) -> None:
        self.server = server
        self.ctrl = server.controller
        self.state = server.state
        self.state.active_ui = None
        self.state.active_view = 0
        self.source_manager = source_manager
        self.visible_manager = visible_manager
        self.data_holder = data_holder
        self.state.pipeline = self.initialize_state_pipeline(1)
        self.state.pipeline_key = 0

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------
    def pipeline_widget(self):
        with vuetify.VContainer():
            trame.GitTree(
                sources=(
                    "pipeline",
                    # [
                    #     {"id": "1", "parent": "0", "visible": 1, "name": "Mesh"},
                    #     {"id": "2", "parent": "1", "visible": 1, "name": "Contour"},
                    # ]
                ),
                actives_change=(self.actives_change, "[$event]"),
                visibility_change=(self.visibility_change, "[$event]"),
            )
        vuetify.VDivider(classes="mb-2")

    # -----------------------------------------------------------------------------
    # GUI Components Callbacks
    # -----------------------------------------------------------------------------

    def actives_change(self, ids):
        for item in self.state.pipeline:
            if item["id"] == ids[0]:
                print("find")
                if self.state.active_view:
                    self.data_holder.get_data(int(self.state.active_view)).write_in()
                self.data_holder.get_data(int(ids[0])).read_out()
                self.state.active_ui = item.get("type")
                self.state.active_view = int(ids[0])
                self.state.flush()
                return
        self.state.active_ui = None
        self.state.active_view = 0

    def visibility_change(self, event):
        id = event['id']
        visible = event['visible']
        for item in self.state.pipeline:
            if item["id"] == id:
                if visible:
                    item["visible"] = 1
                else:
                    item["visible"] = 0
                break
        self.visible_manager.set_visible(int(id), visible)

    def initialize_state_pipeline(self, new_main_id: int):
        self.state.active_ui = None
        self.state.active_view = 0
        return [
            {"id": str(new_main_id), "parent": "0", "visible": 1, "name": str(self.state.main_module_name), "type": CardType.Main},
        ]
