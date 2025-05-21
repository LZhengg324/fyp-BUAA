import os
import subprocess
import sys
import time
import argparse
import socket

import paraview.web.venv  # Available in PV 5.10

from trame.app import get_server
from trame.modules import trame
from trame.widgets import vuetify3 as vuetify, paraview, html, client

from src.components.Drawer.UICardManager.DataHolder.DataHolder import DataHolder
from src.components.Drawer.UICardManager.UICardType.ContourCard import ContourCard
from src.components.Drawer.UICardManager.UICardType.GlyphCard import GlyphCard
from src.components.Drawer.UICardManager.UICardType.MainCard import MainCard
from src.components.Drawer.UICardManager.UICardType.SliceCard import SliceCard
from src.components.Drawer.UICardManager.UICardType.StreamTracerCard import StreamTracerCard
from src.components.Drawer.UICardManager.UICardType.ThresholdCard import ThresholdCard
from src.components.Toolbar.PointDataSelector import PointDataSelector
from src.components.Toolbar.StandardButton import StandardButton
from src.components.Toolbar.TimeStep import TimeStep
from src.components.Drawer.PipelineWidget import PipelineWidget
from src.manager.SourceManager import SourceManager
from src.manager.VisibleManager import VisibleManager
from src.file_processor.FileProcessor import FileProcess
from paraview import simple
from trame_vuetify.ui.vuetify3 import SinglePageWithDrawerLayout
from pathlib import Path

from src.utils.IframeManager import IframeManager

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

# 本地
# try:
#     pid = os.getpid()
#     hostname = os.uname().nodename
#     # os.system(f"/opt/paraview/bin/mpiexec -np 16 /opt/paraview/bin/pvserver -p {pid}")
#     # subprocess.Popen([
#     #     "$TRAME_PARAVIEW/bin/mpiexec",
#     #     "-np", "$PARAVIEW_PVSERVER_THREADS",
#     #     "$TRAME_PARAVIEW/bin/pvserver",
#     #     "-p", str(pid)
#     # ])
#     subprocess.Popen([
#     os.path.join(os.environ.get("TRAME_PARAVIEW", ""), "bin", "mpiexec"),
#     "-np", os.environ.get("PARAVIEW_PVSERVER_THREADS", "1"),
#     os.path.join(os.environ.get("TRAME_PARAVIEW", ""), "bin", "pvserver"),
#     "-p", str(pid)
#     ])
#     simple.Connect(f"{hostname}", pid)
#     print(server.port)
# except Exception as e:
#     print(e)

# @ctrl.trigger("helloworld")
# def trytry():
#     try:
#         pid = os.getpid()
#         hostname = os.uname().nodename
#         # os.system(f"/opt/paraview/bin/mpiexec -np 16 /opt/paraview/bin/pvserver -p {pid}")
#         subprocess.Popen([
#             "/opt/ParaView-5.12.0-MPI-Linux-Python3.10-x86_64/bin/mpiexec",
#             "-np", "4",
#             "/opt/ParaView-5.12.0-MPI-Linux-Python3.10-x86_64/bin/pvserver",
#             "-p", str(pid)
#         ])
#         simple.Connect(f"{hostname}", pid)
#         print(server.port)
#     except Exception as e:
#         print(e)


def check_port_in_use(port, host='127.0.0.1'):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()

parser = argparse.ArgumentParser(
    prog='$TRAME_PARAVIEW/bin/pvpython',  # 程序名
)
# parser.add_argument('filename')  # 位置参数
# 本地
# parser.add_argument('--venv')  # 接受一个值的选项
# parser.add_argument('--port')  # 接受一个值的选项
# print(f"port: {parser.parse_args().port}")
# print(f"venv: {parser.parse_args().venv}")

# Docker的
parser.add_argument('--host')
parser.add_argument('--port')
parser.add_argument('--authKey')
parser.add_argument('--server', action='store_true', required=False)
print(f"host: {parser.parse_args().host}")
print(f"port: {parser.parse_args().port}")
print(f"authKey: {parser.parse_args().authKey}")
print(f"server: {parser.parse_args().server}")

port = int(parser.parse_args().port) + 2111
while True:
    if not check_port_in_use(port):
        break
    port += 1

try:
    pid = os.getpid()
    hostname = os.uname().nodename
    subprocess.Popen([
        os.path.join(os.environ.get("TRAME_PARAVIEW", ""), "bin", "mpiexec"),
        "-np", os.environ.get("PARAVIEW_PVSERVER_THREADS", "1"),
        os.path.join(os.environ.get("TRAME_PARAVIEW", ""), "bin", "pvserver"),
        "-p", str(port)
    ])
    simple.Connect(f"{hostname}", port)
    print(server.port)
except Exception as e:
    print(e)

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
state.received_messages = []

@ctrl.trigger("start_new_module")
def start_new_module(file_path: Path):
    try:
        time1 = time.time()
        print("time1:", time1)
        # Source Manager
        source_manager.reboot_all_for_new_main_module()
        time2 = time.time()
        print("time2 - time1: ", time2 - time1)
        # Visible Manager
        visible_manager.reboot_all_for_new_main_module()
        time3 = time.time()
        print("time3 - time2: ", time3 - time2)
        # Data Holder
        data_holder.reboot_all_for_new_main_module()
        time4 = time.time()
        print("time4 - time3: ", time4 - time3)
        # File Process
        new_main_module_id = fp.initialize_app(file_path=file_path)
        time5 = time.time()
        print("finish read: ", time5 - time4)
        # Pipeline Widget
        state.pipeline = pipeline_widget.initialize_state_pipeline(new_main_module_id)
        print("pipeline", state.pipeline)
        time6 = time.time()
        print("time6 - time5", time6 - time5)
        visible_manager.initialize_lookup_table(new_main_module_id)
        time7 = time.time()
        print("finish render", time7 - time6)
        visible_manager.set_visible(new_main_module_id, True)
        time8 = time.time()
        print("time8 - time7", time8 - time7)
    except Exception as e:
        err = e.args[0] if e.args and isinstance(e.args[0], dict) else {}
        print(err)
        state.invalid_msg = err['msg']
        state.error_catch = True
    state.reboot_all_for_new_main_module = False
    ctrl.view_reset_camera()
    with state:
        state.file_upload_dialog = False
        state.loading = False
        state.selected = []

# -----------------------------------------------------------------------------
# ToolBar's GUI Components
# -----------------------------------------------------------------------------

point_data_selector = PointDataSelector(server=server, visible_manager=visible_manager)
# time_step = TimeStep(server, visible_manager)
standard_button = StandardButton(server=server, file_process=fp)

# -----------------------------------------------------------------------------
# Drawer's GUI Components
# -----------------------------------------------------------------------------

pipeline_widget = PipelineWidget(server=server, source_manager=source_manager,
                                 visible_manager=visible_manager, data_holder=data_holder)
main_card = MainCard(server=server, source_manager=source_manager,
                     visible_manager=visible_manager, data_holder=data_holder)
slice_card = SliceCard(server=server, source_manager=source_manager,
                       visible_manager=visible_manager, data_holder=data_holder)
contour_card = ContourCard(server=server, source_manager=source_manager,
                           visible_manager=visible_manager, data_holder=data_holder)
glyph_card = GlyphCard(server=server, source_manager=source_manager,
                       visible_manager=visible_manager, data_holder=data_holder)
streamtracer_card = StreamTracerCard(server=server, source_manager=source_manager,
                                    visible_manager=visible_manager, data_holder=data_holder)
threshold_card = ThresholdCard(server=server, source_manager=source_manager,
                               visible_manager=visible_manager, data_holder=data_holder)

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

# @ctrl.add("on_client_connected")
# def func():
#     print(f"Life cycle: on server ready")
#     print(f"View ID: {render_view.GetGlobalIDAsString()}")
#     print(server.port)
#     try:
#         port = server.port + 2111
#         hostname = os.uname().nodename
#         # os.system(f"/opt/paraview/bin/mpiexec -np 16 /opt/paraview/bin/pvserver -p {pid}")
#         subprocess.Popen([
#             "/opt/ParaView-5.12.0-MPI-Linux-Python3.10-x86_64/bin/mpiexec",
#             "-np", "2",
#             "/opt/ParaView-5.12.0-MPI-Linux-Python3.10-x86_64/bin/pvserver",
#             "-p", str(port)
#         ])
#         simple.Connect(f"{hostname}", port)
#         print(server.port)
#     except Exception as e:
#         print(e)


def client_exited():
    print("client exited")

with SinglePageWithDrawerLayout(server, theme=("theme_mode", "light")) as layout:
    iframe_manager.register()
    # client_triggers = client.ClientTriggers(
    #     ref="ref_name",
    #     mounted=(monitor_life_cycles, "['created']"),
    #     # mounted=(monitor_life_cycles, "['mounted']"),
    #     # beforeDestroy=(monitor_life_cycles, "['beforeDestroy']"),
    #     # destroyed=(monitor_life_cycles, "['destroyed']"),
    # )
    with layout.toolbar as toolbar:
        # vuetify.VBtn(
        #     "button",
        #     click="trigger('helloworld')"
        # )
        point_data_selector.point_data_selector()
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
        with vuetify.VSnackbar(
                v_model=("error_catch", False),
                width="400px",
                timeout=5000,
                color="error",
                location="bottom right"
        ):
            vuetify.VIcon(
                icon="mdi-alert-circle-outline",
                classes="mr-1",
                hide_details=True,
            )
            html.Span(
                "{{invalid_msg}}",
                color="#ffffff",
                style="font-size: 16px; align-items: center;",
            )
        view = paraview.VtkRemoteView(render_view)
        # view = paraview.VtkLocalView(render_view)
        ctrl.view_update = view.update
        ctrl.view_reset_camera = view.reset_camera
        ctrl.view_reset_camera()
    # client.LifeCycleMonitor(type="info", events=("['created']",))

# 8. 启动服务器
if __name__ == '__main__':
    server.start(host="127.0.0.1")
    simple.Disconnect()
    print("exit...")
