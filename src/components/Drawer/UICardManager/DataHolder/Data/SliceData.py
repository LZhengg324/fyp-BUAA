from typing import Tuple

from trame_server import Server

from .Data import Data


class SliceData(Data):
    def __init__(self, data_id: int, name: str, server: Server, slice_default_origin: Tuple[float, float, float]):
        super().__init__(data_id=data_id, name=name, server=server)
        self.Origin_x = slice_default_origin[0]
        self.Origin_y = slice_default_origin[1]
        self.Origin_z = slice_default_origin[2]
        # Normal = [nx, ny, nz]
        # origin = [x0, y0, z0]
        # nx(x - x0) + ny(y - y0) + nz(z - z0) = 0
        self.Normal_x = 1
        self.Normal_y = 0
        self.Normal_z = 0
        self.Type = "Plane"

    def write_in(self):
        print("slice_son write")
        self.Origin_x = self.state.Slice_Origin_x
        self.Origin_y = self.state.Slice_Origin_y
        self.Origin_z = self.state.Slice_Origin_z
        self.Normal_x = self.state.Slice_Normal_x
        self.Normal_y = self.state.Slice_Normal_y
        self.Normal_z = self.state.Slice_Normal_z
        self.Type = self.state.Slice_Type
        pass

    def read_out(self):
        print("slice_son read")
        super().read_out()
        self.state.Slice_Origin_x = self.Origin_x
        self.state.Slice_Origin_y = self.Origin_y
        self.state.Slice_Origin_z = self.Origin_z
        self.state.Slice_Normal_x = self.Normal_x
        self.state.Slice_Normal_y = self.Normal_y
        self.state.Slice_Normal_z = self.Normal_z
        self.state.Slice_Type = self.Type
        self.state.flush()
        pass

    def get_normal(self):
        return [self.Normal_x, self.Normal_y, self.Normal_z]

    def get_origin(self):
        return [self.Origin_x, self.Origin_y, self.Origin_z]

    def get_module_name(self) -> str:
        return super().get_module_name()

    def rename_module(self, new_name: str):
        super().rename_module(new_name)