from copy import deepcopy
from typing import Tuple, List, Dict

from trame_server import Server

class Data:
    def __init__(self, name: str, data_id: int, server: Server):
        self.name = name
        self.data_id = data_id
        self.nt_available_delete = False
        self.server = server
        self.state = self.server.state

    def write_in(self):
        print("father write")
        pass

    def read_out(self):
        self.state.nt_available_delete = self.data_nt_available_delete()
        self.state.module_name = self.get_module_name()

    def get_module_name(self):
        return self.name

    def rename_module(self, new_name: str):
        self.name = new_name

    def get_slice_default_origin(self) -> Tuple[float, float, float]:
        pass

    def get_normal(self):
        pass

    def data_nt_available_delete(self) -> bool:
        for item in self.state.pipeline:
            if item["parent"] == str(self.data_id):
                return True
        return False


