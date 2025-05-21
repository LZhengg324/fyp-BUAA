from copy import deepcopy

from trame_server import Server

from .Data import Data


class ContourData(Data):
    def __init__(self, data_id: int, name: str, server: Server, slice_data: Data):
        super().__init__(data_id=data_id, name=name, server=server)
        self.slice_data = slice_data
        self.Isosurfaces = {}
        for ss in self.state.scalar_fields:
            value = (self.state.point_data_range[ss][0] + self.state.point_data_range[ss][1]) / 2
            self.Isosurfaces[ss] = [{"title": str(value), "value": value}, ]
        self.contour_by = ""
        print("Isosurfaces : ", self.Isosurfaces)

    def write_in(self):
        self.Isosurfaces.clear()
        self.Isosurfaces = deepcopy(self.state.Isosurfaces)
        self.contour_by = self.state.Contour_contour_by
        print("contour_son write", self.Isosurfaces)

    def read_out(self):
        super().read_out()
        self.state.Isosurfaces.clear()
        self.state.Isosurfaces = deepcopy(self.Isosurfaces)
        self.state.Contour_contour_by = self.contour_by
        print("contour_son read", self.state.Isosurfaces)

    def get_module_name(self) -> str:
        return super().get_module_name()

    def rename_module(self, new_name: str):
        super().rename_module(new_name)