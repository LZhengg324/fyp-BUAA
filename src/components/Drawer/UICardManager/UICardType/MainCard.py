from trame_server import Server

from src.components.Drawer.UICardManager.DataHolder import DataHolder
from src.constants.CardType import CardType
from src.manager.SourceManager import SourceManager
from src.manager.VisibleManager import VisibleManager
from src.components.Drawer.UICardManager.UICard import UICard
from trame.widgets import vuetify3 as vuetify

class MainCard:
    def __init__(self, server: Server,
                 source_manager: SourceManager, visible_manager: VisibleManager,
                 data_holder: DataHolder):
        self.source_manager = source_manager
        self.visible_manager = visible_manager
        self.data_holder = data_holder
        self.server = server
        self.state = server.state
        self.ctrl = server.controller

        # -----------------------------------------------------------------------------
        # Register Callbacks
        # -----------------------------------------------------------------------------

        self.ctrl.create_slice_view = self.create_slice_view
        self.ctrl.create_threshold_view = self.create_threshold_view

        # @self.ctrl.trigger("create_slice_view")
        # def create_slice_view():
        #     new_view_id = self.source_manager.add_slice(source_id=self.state.active_view)
        #     self.state.pipeline = (self.state.pipeline +
        #                            [{"id": str(new_view_id), "parent": str(self.state.active_view),
        #                              "visible": 0, "name": "Slice", "type": CardType.Slice}, ])
        #     self.data_holder.register(name="Slice", source_id=new_view_id, card_type=CardType.Slice,
        #                               parent_idx=self.state.active_view)

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------
    def show_card(self):
        with UICard(card_type=CardType.Main, data_holder=self.data_holder).ui_card():
            with vuetify.VRow():
                with vuetify.VCol():
                    vuetify.VBtn(
                        "Slice",
                        classes="ma-1",
                        width="100%",
                        # click="trigger('create_slice_view')",
                        click=self.ctrl.create_slice_view,
                    )
            with vuetify.VRow():
                with vuetify.VCol():
                    vuetify.VBtn(
                        "Threshold",
                        classes="ma-1",
                        width="100%",
                        click=self.ctrl.create_threshold_view,
                    )


    # -----------------------------------------------------------------------------
    # GUI Callbacks
    # -----------------------------------------------------------------------------

    def create_slice_view(self):
        new_view_id = self.source_manager.add_slice(source_id=self.state.active_view)
        self.state.pipeline = (self.state.pipeline +
                               [{"id": str(new_view_id), "parent": str(self.state.active_view),
                                 "visible": 0, "name": "Slice", "type": CardType.Slice}, ])
        self.data_holder.register(name="Slice", source_id=new_view_id, card_type=CardType.Slice, parent_idx=self.state.active_view)

    def create_threshold_view(self):
        new_view_id = self.source_manager.add_threshold(source_id=self.state.active_view)
        self.state.pipeline = (self.state.pipeline +
                               [{"id": str(new_view_id), "parent": str(self.state.active_view),
                                 "visible": 0, "name": "Threshold", "type": CardType.Threshold}, ])
        self.data_holder.register(name="Threshold", source_id=new_view_id, card_type=CardType.Threshold,
                                  parent_idx=self.state.active_view)