import asyncio
import os
import zipfile
from pathlib import Path

from trame.widgets import vuetify3 as vuetify, trame
from trame_server import Server
from trame.app import asynchronous

from src.manager.VisibleManager import VisibleManager

class PointDataSelector:
    def __init__(self, server: Server, visible_manager: VisibleManager):
        self.server = server
        self.ctrl = server.controller
        self.state = server.state
        self.visible_manager = visible_manager

        @self.state.change("cur_mesh")
        def update_mesh_type(cur_mesh, **kwargs):
            if cur_mesh:
                self.visible_manager.mesh_or_point_data_update()

        @self.state.change("cur_point_data")
        def update_scalar_field(cur_point_data, **kwargs):
            if cur_point_data:
                self.visible_manager.mesh_or_point_data_update()

    def point_data_selector(self):
        vuetify.VSelect(
            # Color By
            label="Mesh",
            v_model=("cur_mesh",),
            items=("mesh_types",),
            hide_details=True,
            classes="pa-1",
            variant="outlined",
            style="max-width: 180px;",
        )
        vuetify.VSelect(
            # Color Map
            label="Point Data Fields",
            v_model=("cur_point_data",),
            items=("point_data_fields",),
            hide_details=True,
            classes="pa-1",
            variant="outlined",
            style="max-width: 180px;",
        )