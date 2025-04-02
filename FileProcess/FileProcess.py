import os
import shutil
import zipfile

import paraview.web.venv  # Available in PV 5.10

from trame.widgets import vuetify3 as vuetify, paraview
from trame_server import Server

from Components.Drawer.UICardManager.DataHolder import DataHolder
from Constants.card_type import CardType
from Source.SourceManager import SourceManager
from paraview import simple
from trame_vuetify.ui.vuetify3 import SinglePageWithDrawerLayout

import re
from pathlib import Path

WRITE_FILE_DIRECTORY = Path(__file__).resolve().parent.parent.joinpath('File')
READ_FILE_DIRECTORY = Path(__file__).resolve().parent.parent.joinpath('File').joinpath("host").joinpath("VTK")

class FileProcess:
    def __init__(self, server: Server, source_manager: SourceManager, data_holder: DataHolder):
        self.server = server
        self.state = server.state
        self.source_manager = source_manager
        self.data_holder = data_holder

        self.state.reboot_all_for_new_main_module = False

        @self.state.change("reboot_all_for_new_main_module")
        def reboot_all_for_new_main_module(reboot_all_for_new_main_module, **kwargs):
            if reboot_all_for_new_main_module:
                pass


    def initialize_app(self, filename: str, directory: Path):
        vtk_files = list(directory.glob("*_*.vtk"))
        print("vtk_files:", vtk_files)
        writeInterval = []
        file_readers = dict()
        for vtk_file in vtk_files:
            match = re.search(r"([A-Za-z0-9]+)_(\d+)\.vtk", str(vtk_file))
            if match:
                name = match.group(1)
                num = int(match.group(2))
                print(name, num)
                if num == 0:
                    continue
                self.state.main_module_name = name
                writeInterval.append(num)
                reader = simple.LegacyVTKReader(FileNames=[str(vtk_file)])
                reader.UpdatePipeline()
                file_readers[num] = reader

        # Time Step
        writeInterval.sort()
        self.state.write_interval = writeInterval
        self.state.cur_step_ptr = 0
        self.state.cur_step = self.state.write_interval[self.state.cur_step_ptr]
        # self.state.min_time_step = min(writeInterval)
        # self.state.max_time_step = max(writeInterval)
        # self.state.step = (max(writeInterval) - min(writeInterval)) // (len(writeInterval) - 1)

        # Main Card
        self.state.data_bounds = file_readers[self.state.cur_step].GetDataInformation().GetBounds()
        main_block_id = self.source_manager.add_source(file_readers)
        self.data_holder.register(name=self.state.main_module_name, source_id=main_block_id, card_type=CardType.Main, data_bounds=self.state.data_bounds)

        # Scalar Field
        self.state.point_data_fields, self.state.point_data_range = self.source_manager.get_point_data_field_and_range(main_block_id)
        self.state.scalar_fields, self.state.vector_field = self.source_manager.get_scalar_vector_field_and_range(main_block_id)
        self.state.cur_point_data = self.state.point_data_fields[0]

        # Mesh Field
        self.state.setdefault("cur_mesh", "POINTS")
        self.state.setdefault("mesh_types", [
            {"title": "Points", "value": "POINTS"},
            {"title": "Cells", "value": "CELLS"},
        ])
        return main_block_id

    def write_file(self):
        # Make Sure Exists Base Directory
        WRITE_FILE_DIRECTORY.mkdir(parents=True, exist_ok=True)

        # Create User Process Directory
        process_dir = WRITE_FILE_DIRECTORY.joinpath(f"process_{os.getpid()}")
        if process_dir.exists():
            shutil.rmtree(process_dir)
        process_dir.mkdir(exist_ok=True)

        # Check File Content Exists
        if not self.state.file_input or "content" not in self.state.file_input.keys():
            raise ValueError("No file content received!")

        content = self.state.file_input["content"]
        if isinstance(content, str) and content.startswith("data:"):
            # 移除可能的MIME类型前缀（如：data:application/zip;base64,）
            content = content.split(",", 1)[1]

        # write zip file
        zip_path = process_dir.joinpath("upload.zip")
        try:
            if isinstance(content, str):
                # Decode if Base64 String
                import base64
                content = base64.b64decode(content)
            with open(zip_path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise IOError(f"Failed to write file: {e}")

        # zip_path nt a zipfile
        if not zipfile.is_zipfile(zip_path):
            os.remove(zip_path)  # delete invalid zip archive
            raise ValueError("Uploaded file is not a valid ZIP archive")

        # Extract Zip File
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(process_dir)
        except zipfile.BadZipFile:
            raise ValueError("Corrupted ZIP file")
        finally:
            os.remove(zip_path)  # delete temp file

        print(f"File uploaded and extracted to: {process_dir}")

    def initialize_new_module(self):

        new_main_module_id = 0

        # Make Sure Exists Base Directory
        WRITE_FILE_DIRECTORY.mkdir(parents=True, exist_ok=True)

        # Create User Process Directory
        process_dir = WRITE_FILE_DIRECTORY.joinpath(f"process_{os.getpid()}")
        process_dir.mkdir(exist_ok=True)

        vtk_dir = process_dir / "VTK"

        if vtk_dir.exists() and vtk_dir.is_dir():
            process_dir = vtk_dir

        print("process_dir:", process_dir)

        try:
            new_main_module_id = self.initialize_app(filename="host", directory=process_dir)
        except Exception as e:
            raise IOError(f"Failed to write file: {e}")
        print(f"new_main_module_id: {new_main_module_id}")
        return new_main_module_id


