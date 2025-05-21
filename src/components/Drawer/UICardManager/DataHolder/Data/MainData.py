from typing import Tuple

from trame_server import Server

from .Data import Data


class MainData(Data):
    def __init__(self, data_id: int, name: str, server: Server, data_bounds: Tuple[float, float, float, float, float, float]):
        super().__init__(data_id=data_id, name=name, server=server)
        self.DataBounds = tuple(round(num, 5) for num in data_bounds)

    def write_in(self):
        print("son write")
        pass

    def read_out(self):
        print("son read")
        super().read_out()
        pass

    def get_slice_default_origin(self) -> Tuple[float, float, float]:
        x_min, x_max, y_min, y_max, z_min, z_max = self.DataBounds
        return ((x_min + x_max) / 2,
                (y_min + y_max) / 2,
                (z_min + z_max) / 2)

    def get_module_name(self) -> str:
        return super().get_module_name()

    def rename_module(self, new_name: str):
        super().rename_module(new_name)