import os
import shutil
import time
import zipfile
from collections import defaultdict

import paraview.web.venv  # Available in PV 5.10

from trame.widgets import vuetify3 as vuetify, paraview
from trame_server import Server

from src.components.Drawer.UICardManager.DataHolder import DataHolder
from src.constants.CardType import CardType
from src.manager.SourceManager import SourceManager
from paraview import simple
from pathlib import Path
import re

# WRITE_FILE_DIRECTORY = Path(__file__).resolve().parent.parent.joinpath('File')
READ_FILE_DIRECTORY = Path(__file__).resolve().parent.parent.joinpath('CFD_Files')
# READ_FILE_DIRECTORY = Path(__file__).resolve().parent.parent.joinpath('File').joinpath("host").joinpath("VTK")

class FileProcess:
    def __init__(self, server: Server, source_manager: SourceManager, data_holder: DataHolder):
        self.server = server
        self.state = server.state
        self.source_manager = source_manager
        self.data_holder = data_holder

        self.state.reboot_all_for_new_main_module = False
        self.state.point_data_fields = []
        self.state.point_data_range = defaultdict(tuple)
        self.state.scalar_fields = ()
        self.state.vector_field = []
        self.state.cur_point_data = ""
        self.state.mesh_types = []
        self.state.cur_mesh = ""
        self.reader_map = {
            "vtk": lambda path: simple.LegacyVTKReader(FileNames=[str(path)]),
            "vtu": lambda path: simple.XMLUnstructuredGridReader(FileName=str(path)),
            "vtp": lambda path: simple.XMLPolyDataReader(FileName=str(path)),
            "vts": lambda path: simple.XMLStructuredGridReader(FileName=str(path)),
            "vtm": lambda path: simple.XMLMultiBlockDataReader(FileName=str(path)),
            "pvtu": lambda path: simple.XMLPartitionedUnstructuredGridReader(FileName=str(path)),
            "pvts": lambda path: simple.XMLPartitionedStructuredGridReader(FileName=str(path)),
        }

    def select_reader_type(self, file_path: Path):
        suffix = file_path.suffix.lstrip(".")
        if suffix not in self.reader_map:
            raise ValueError({
                'errcode': 1,
                'msg': f"Unsupported file suffix: \".{suffix}\"",
            })
        return self.reader_map[suffix](file_path)

    def initialize_app(self, file_path: Path):
        try:
            reader = self.select_reader_type(file_path)
            reader.UpdatePipeline()
            print(reader)

            # Main Card
            self.state.data_bounds = reader.GetDataInformation().GetBounds()
            print(self.state.data_bounds)

            main_block_id = self.source_manager.add_source(reader)
            self.state.main_module_name = str(file_path.stem)
            self.data_holder.register(name=self.state.main_module_name, source_id=main_block_id, card_type=CardType.Main, data_bounds=self.state.data_bounds)

            # Scalar Field
            self.state.point_data_fields, self.state.point_data_range = self.source_manager.get_point_data_field_and_range(main_block_id)
            self.state.scalar_fields, self.state.vector_field = self.source_manager.get_scalar_vector_field_and_range(main_block_id)
            self.state.cur_point_data = self.state.point_data_fields[0] if self.state.point_data_fields else []

            # Mesh Field
            self.state.mesh_types = [
                {"title": "Points", "value": "POINTS"},
                {"title": "Cells", "value": "CELLS"},
            ]
            self.state.cur_mesh = "POINTS"
        except ValueError or RuntimeError as e:
            raise e
        else:
            return main_block_id
