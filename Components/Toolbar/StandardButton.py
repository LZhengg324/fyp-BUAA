import os
import zipfile

from trame.widgets import vuetify3 as vuetify, trame
from trame_server import Server

from FileProcess.FileProcess import FileProcess


class StandardButton:
    def __init__(self, server: Server, file_process: FileProcess):
        self.server = server
        self.ctrl = server.controller
        self.state = server.state
        self.file_process = file_process

        self.state.file_upload_dialog = False
        self.state.file_input = ""
        self.state.disabled_render_button = True

        @self.state.change("file_input")
        def file_input_changed(file_input, **kwargs):
            if file_input:
                self.state.disabled_render_button = False
            else:
                self.state.disabled_render_button = True

        self.ctrl.open_file_upload_dialog_trigger = self.open_file_upload_dialog_trigger
        self.ctrl.close_file_upload_dialog_trigger = self.close_file_upload_dialog_trigger
        self.ctrl.handle_uploaded_file = self.handle_uploaded_file

    def standard_button(self):
        with vuetify.VDialog(v_model=("file_upload_dialog",), width="500"):
            with vuetify.VCard():
                vuetify.VCardText("File Upload")
                vuetify.VFileInput(
                    variant="outlined",
                    classes="ma-2",
                    v_model=("file_input", ""),
                    accept=".zip",
                    __properties=["accept"],
                )
                vuetify.VBtn(
                    "Render",
                    disabled= ("disabled_render_button",),
                    click=self.ctrl.handle_uploaded_file,
                )
        vuetify.VCheckbox(
            v_model=("theme_mode", "light"),
            true_icon="mdi-weather-night",
            false_icon="mdi-weather-sunny",
            true_value="dark",
            false_value="light",
            classes="mx-1",
            hide_details=True,
            dense=True,
        )
        vuetify.VBtn(
            icon="mdi-file-import",
            click=self.ctrl.open_file_upload_dialog_trigger,
        )
        vuetify.VBtn(
            "update",
            click=self.ctrl.view_update
        )
        vuetify.VBtn(
            icon="mdi mdi-crop-free",
            click=self.ctrl.view_reset_camera
        )

    def open_file_upload_dialog_trigger(self):
        self.state.file_upload_dialog = True

    def close_file_upload_dialog_trigger(self):
        self.state.file_upload_dialog = False

    def handle_uploaded_file(self):
        self.file_process.write_file()
        self.state.reboot_all_for_new_main_module = True
        # self.state.flush()
        # self.file_process.initialize_new_module()
        self.state.file_upload_dialog = False