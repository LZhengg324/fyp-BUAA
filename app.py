import os
import time

import paraview.web.venv  # Available in PV 5.10

from trame.app import get_server
from trame.modules import trame
from trame.widgets import vuetify3 as vuetify, paraview

from Components.Drawer.UICardManager.DataHolder.DataHolder import DataHolder
from Components.Drawer.UICardManager.UICardType.ContourCard import ContourCard
from Components.Drawer.UICardManager.UICardType.GlyphCard import GlyphCard
from Components.Drawer.UICardManager.UICardType.MainCard import MainCard
from Components.Drawer.UICardManager.UICardType.SliceCard import SliceCard
from Components.Drawer.UICardManager.UICardType.StreamTracerCard import StreamTracerCard
from Components.Drawer.UICardManager.UICardType.ThresholdCard import ThresholdCard
from Components.Toolbar.StandardButton import StandardButton
from Constants.card_type import CardType
from Components.Toolbar.TimeStep import TimeStep
from Components.Drawer.PipelineWidget import PipelineWidget
from Source.SourceManager import SourceManager
from Source.VisibleManager import VisibleManager
from FileProcess.FileProcess import FileProcess
from FileProcess.FileProcess import READ_FILE_DIRECTORY
from paraview import simple
from trame_vuetify.ui.vuetify3 import SinglePageWithDrawerLayout
from pathlib import Path

from utils.IframeManager import IframeManager

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------
# trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue3")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

render_view = simple.GetActiveViewOrCreate('RenderView')
data_holder = DataHolder(server=server)
source_manager = SourceManager()
visible_manager = VisibleManager(server=server, source_manager=source_manager, render_view=render_view)
fp = FileProcess(server, source_manager, data_holder)
iframe_manager = IframeManager(server=server)
iframe_manager.add_event("post_message_to_iframe", received_messages)
iframe_manager.add_event("post_file_name_to_iframe", read_file)
# main_block_id = fp.initialize_app("host", READ_FILE_DIRECTORY)
# main_block_id = fp.initialize_app(READ_FILE_DIRECTORY.joinpath("host2").joinpath("VTK").joinpath("host_40.vtk"))
state.received_messages = []
# state.file_content = ""

# -----------------------------------------------------------------------------
# State Ref
# -----------------------------------------------------------------------------

state.setdefault("file_upload_dialog", False)

# -----------------------------------------------------------------------------
# Controller triggers
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# State Callbacks
# -----------------------------------------------------------------------------

@state.change("cur_mesh")
def update_mesh_type(cur_mesh, **kwargs):
    if cur_mesh:
        visible_manager.mesh_or_point_data_update()

@state.change("cur_point_data")
def update_scalar_field(cur_point_data, **kwargs):
    if cur_point_data:
        visible_manager.mesh_or_point_data_update()

@state.change("file_input")
def update_file_input(file_input, **kwargs):
    # state.uploading = True
    pass
    # state.uploading = False

@state.change("reboot_all_for_new_main_module")
def update_reboot_all_for_new_main_module(reboot_all_for_new_main_module, **kwargs):
    if reboot_all_for_new_main_module:
        try:
            time1 = time.time()
            print("time1:", time1)
            # Source Manager
            source_manager.reboot_all_for_new_main_module()
            time2 = time.time()
            print("time2 - time1: ", time2-time1)
            # Visible Manager
            visible_manager.reboot_all_for_new_main_module()
            time3 = time.time()
            print("time3 - time2: ", time3-time2)
            # Data Holder
            data_holder.reboot_all_for_new_main_module()
            time4 = time.time()
            print("time4 - time3: ", time4-time3)
            # File Process
            # new_main_module_id = fp.initialize_new_module()
            new_main_module_id = fp.initialize_app(Path(state.selected[0]))
            time5 = time.time()
            print("time5 - time4", time5-time4)
            # Pipeline Widget
            state.pipeline = pipeline_widget.initialize_state_pipeline(new_main_module_id)
            time6 = time.time()
            print("time6 - time5", time6 - time5)
            visible_manager.initialize_lookup_table(new_main_module_id)
            time7 = time.time()
            print("time7 - time6", time7 - time6)
            visible_manager.set_visible(new_main_module_id, True)
            time8 = time.time()
            print("time8 - time7", time8 - time7)
        except Exception as e:
            print(e)
        state.reboot_all_for_new_main_module = False
        ctrl.view_reset_camera()
        state.file_upload_dialog = False
        state.loading = False
        print("Finish:", time8-time1)


# -----------------------------------------------------------------------------
# ToolBar's GUI Components
# -----------------------------------------------------------------------------

time_step = TimeStep(server, visible_manager)
standard_button = StandardButton(server, fp)

# -----------------------------------------------------------------------------
# Drawer's GUI Components
# -----------------------------------------------------------------------------

pipeline_widget = PipelineWidget(server=server, source_manager=source_manager, visible_manager=visible_manager, data_holder=data_holder)
main_card = MainCard(card_name="host", server=server, source_manager=source_manager,
                     visible_manager=visible_manager, data_holder=data_holder)
slice_card = SliceCard(card_name="Slice", server=server, source_manager=source_manager,
                       visible_manager=visible_manager, data_holder=data_holder)
contour_card = ContourCard(card_name="Contour", server=server, source_manager=source_manager,
                           visible_manager=visible_manager, data_holder=data_holder)
glyph_card = GlyphCard(card_name="Glyph", server=server, source_manager=source_manager,
                       visible_manager=visible_manager, data_holder=data_holder)
streamtracer_card = StreamTracerCard(card_name="Stream Tracer", server=server, source_manager=source_manager,
                                    visible_manager=visible_manager, data_holder=data_holder)
threshold_card = ThresholdCard(card_name="Threshold", server=server, source_manager=source_manager,
                               visible_manager=visible_manager, data_holder=data_holder)

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageWithDrawerLayout(server, theme=("theme_mode", "light")) as layout:
    iframe_manager.register()
    with layout.toolbar as toolbar:
        vuetify.VSelect(
            # Color By
            label="Mesh",
            v_model=("cur_mesh",),
            items=("mesh_types", ),
            hide_details=True,
            classes="pa-1",
            variant="outlined",
            style="max-width: 180px;",
        )
        vuetify.VSelect(
            # Color Map
            label="Point Data Fields",
            v_model=("cur_point_data",),
            items=("point_data_fields", ),
            hide_details=True,
            classes="pa-1",
            variant="outlined",
            style="max-width: 180px;",
        )
        vuetify.VSpacer()
        # time_step.time_step()
        vuetify.VDivider(
            vertical=True,
            classes="mx-2"
        )
        standard_button.standard_button()

    with layout.drawer as drawer:
        drawer.width = 350
        pipeline_widget.pipeline_widget()
        with vuetify.VContainer(classes="pa-1"):
            main_card.show_card()
            slice_card.show_card()
            contour_card.show_card()
            glyph_card.show_card()
            streamtracer_card.show_card()
            threshold_card.show_card()

    with layout.content:
        view = paraview.VtkRemoteView(render_view)
        # view = paraview.VtkLocalView(render_view)
        ctrl.view_update = view.update
        ctrl.view_reset_camera = view.reset_camera
        # visible_manager.initialize_lookup_table(main_block_id=main_block_id)
        # visible_manager.set_visible(main_block_id, True)
        ctrl.view_reset_camera()

# 8. 启动服务器
if __name__ == '__main__':
    simple.Connect("LAPTOP-EA0G2BQO")
    server.start(host="127.0.0.1")
