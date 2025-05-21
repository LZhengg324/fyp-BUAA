from typing import List, Dict

from trame.app import get_server
from trame.widgets import vuetify3 as vuetify, trame
from trame_server import Server

from src.components.Drawer.UICardManager.DataHolder.DataHolder import DataHolder
from src.constants.CardType import CardType
from paraview import simple


class UICard:
    def __init__(self, card_type: CardType, data_holder: DataHolder):
        self.server = get_server()
        self.ctrl, self.state = self.server.controller, self.server.state
        self.card_type = card_type
        self.data_holder = data_holder
        self.state.rename_dialog = False
        self.state.module_name = ""

        # -----------------------------------------------------------------------------
        # CallBacks Register
        # -----------------------------------------------------------------------------

        self.ctrl.open_rename_dialog = self.open_rename_dialog
        self.ctrl.close_rename_dialog = self.close_rename_dialog
        self.ctrl.rename_module = self.rename_module

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------
    def ui_card(self):
        with vuetify.VDialog(
                v_model=("rename_dialog",),
                width="400",
                height="200",
        ):
            with vuetify.VCard():
                vuetify.VCardTitle(
                    "Rename Module",
                    classes="my-2 font-weight-bold text-black",
                )
                vuetify.VTextField(
                    label="New Name",
                    v_model=("module_new_name", ),
                    classes="mx-2",
                    variant="outlined"
                )
                vuetify.VBtn(
                    "Rename",
                    # disabled= ("uploading",),
                    click=self.ctrl.rename_module,
                    classes="mt-2",
                    density="comfortable",
                    hide_details=True,
                )
        with vuetify.VCard(v_show=f"active_ui == {self.card_type}"):
            with vuetify.VRow(
                classes="my-2",
            ):
                vuetify.VCardTitle(
                    "{{module_name}}",
                    classes="grey lighten-1 py-1 ml-3 mr-1 grey--text text--darken-3",
                    style="user-select: none;",
                    hide_details=True,
                    dense=True,
                )
                vuetify.VIcon(
                    icon="mdi mdi-pencil-outline",
                    click=self.ctrl.open_rename_dialog,
                    end=True,
                    size="x-small",
                    style="align-self: center; cursor: pointer",
                    clickable=True,
                )
            content = vuetify.VCardText()
        return content

    def open_rename_dialog(self):
        self.state.rename_dialog = True
        self.state.module_new_name = self.state.module_name

    def close_rename_dialog(self):
        self.state.rename_dialog = False

    def rename_module(self):
        for idx, item in enumerate(self.state.pipeline):
            if int(item["id"]) == self.state.active_view:
                new_item = self.state.pipeline.pop(idx)
                new_item["name"] = self.state.module_new_name
                data = self.data_holder.get_data(self.state.active_view)
                data.rename_module(self.state.module_new_name)
                self.state.module_name = self.state.module_new_name
                self.state.pipeline = self.state.pipeline + [new_item]
                self.state.rename_dialog = False
                return