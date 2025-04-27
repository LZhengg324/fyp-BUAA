import os
import zipfile
from pathlib import Path

from trame.widgets import vuetify3 as vuetify, trame
from trame_server import Server

from FileProcess.FileProcess import FileProcess
from FileProcess.FileProcess import READ_FILE_DIRECTORY


class StandardButton:
    def __init__(self, server: Server, file_process: FileProcess):
        self.server = server
        self.ctrl = server.controller
        self.state = server.state
        self.file_process = file_process
        self.root_directory = READ_FILE_DIRECTORY

        self.state.file_upload_dialog = False
        self.state.file_input = ""
        self.state.disabled_render_button = True
        self.state.color_bar_visibility = True
        self.state.tree_items = self.build_tree(self.root_directory)
        self.state.selected = []
        self.state.active_node = []
        self.state.loading = False

        @self.state.change("selected")
        def update_treeview_items(selected, **kwargs):
            print("selected:", selected)
            self.state.active_node = selected
            if selected:
                self.state.disabled_render_button = False
            else:
                self.state.disabled_render_button = True

        # @self.state.change("file_input")
        # def file_input_changed(file_input, **kwargs):
        #     if file_input:
        #         self.state.disabled_render_button = False
        #     else:
        #         self.state.disabled_render_button = True

        self.ctrl.open_file_upload_dialog_trigger = self.open_file_upload_dialog_trigger
        self.ctrl.close_file_upload_dialog_trigger = self.close_file_upload_dialog_trigger
        self.ctrl.handle_uploaded_file = self.handle_uploaded_file
        self.ctrl.set_color_bar = self.set_color_bar
        vuetify.enable_lab()

    def standard_button(self):
        with vuetify.VDialog(v_model=("file_upload_dialog",), width="500"):
            with vuetify.VCard():
                vuetify.VCardText("File Upload")
                vuetify.VTreeview(
                    items=("tree_items", ),
                    item_title="title",
                    item_value="id",
                    item_children="children",
                    v_model=("selected", []),
                    activated=("selected", []),
                    open_on_click = True
                )
                # vuetify.VFileInput(
                #     variant="outlined",
                #     classes="ma-2",
                #     v_model=("file_input", ""),
                #     accept=".zip",
                #     __properties=["accept"],
                # )
                vuetify.VBtn(
                    "Render",
                    disabled= ("disabled_render_button",),
                    click=self.ctrl.handle_uploaded_file,
                    loading=("loading", ),
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
        vuetify.VCheckbox(
            v_model=("color_bar_visibility", ),
            true_icon="mdi-eye-outline",
            false_icon="mdi-eye-closed",
            classes="mx-1",
            hide_details=True,
            dense=True,
            # click=self.ctrl.set_color_bar,
        )
        vuetify.VBtn(
            icon="mdi mdi-crop-free",
            click=self.ctrl.view_reset_camera
        )

    def open_file_upload_dialog_trigger(self):
        self.state.tree_items = self.build_tree(self.root_directory)
        # self.state.dirty("treeview_items")
        self.state.file_upload_dialog = True

    def close_file_upload_dialog_trigger(self):
        self.state.file_upload_dialog = False

    def handle_uploaded_file(self):
        # self.file_process.write_file()
        # self.state.reboot_all_for_new_main_module = True
        # self.state.flush()
        # self.file_process.initialize_new_module()
        # print(self.state.selected)
        # print(self.state.file_input)
        self.state.loading = True
        self.state.reboot_all_for_new_main_module = True
        # self.state.file_upload_dialog = False

    def set_color_bar(self):
        self.state.color_bar_visibility = not self.state.color_bar_visibility

    def build_tree(self, path: Path):
        items = []
        for child in path.iterdir():
            node = {"id": str(child), "title": child.name}
            if child.is_dir():
                node["children"] = self.build_tree(child)
            items.append(node)
        return items
