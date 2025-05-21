from math import sqrt

from trame_server import Server

from .SliceData import SliceData
from .Data import Data


class StreamTracerData(Data):
    def __init__(self, data_id: int, name: str, server: Server, slice_data: SliceData):
        super().__init__(data_id=data_id, name=name, server=server)
        self.slice_data = slice_data
        self.Vectors = self.state.vector_field[0] if self.state.vector_field else None
        self.IntegrationDirection = self.state.ST_IntegrationDirection_List[-1]
        self.IntegratorType = self.state.ST_IntegratorType_List[-1]
        self.MSL = max(self.state.data_bounds[i] for i in range(1, len(self.state.data_bounds), 2))
        self.MSL_value = self.state.ST_MSL
        self.DiagLength = sqrt(sum((self.state.data_bounds[i] - self.state.data_bounds[i - 1]) ** 2
                                            for i in range(1, len(self.state.data_bounds), 2)))
        default_point = self.default_point1_and_point2(slice_data.get_normal(), slice_data.get_origin())
        self.Point1_x, self.Point1_y, self.Point1_z = default_point[0]
        self.Point2_x, self.Point2_y, self.Point2_z = default_point[1]
        self.Resolution = 1000

    def write_in(self):
        self.Vectors = self.state.ST_Vectors
        self.IntegrationDirection = self.state.ST_IntegrationDirection
        self.IntegratorType = self.state.ST_IntegratorType
        self.MSL = self.state.ST_MSL
        self.MSL_value = self.state.ST_MSL_value
        self.DiagLength = self.state.ST_DiagLength
        self.Resolution = self.state.ST_Resolution
        self.Point1_x = self.state.ST_Point1_x
        self.Point1_y = self.state.ST_Point1_y
        self.Point1_z = self.state.ST_Point1_z
        self.Point2_x = self.state.ST_Point2_x
        self.Point2_y = self.state.ST_Point2_y
        self.Point2_z = self.state.ST_Point2_z
        print("stream_son write")

    def read_out(self):
        normal = self.slice_data.get_normal()
        origin = self.slice_data.get_origin()
        super().read_out()
        self.state.Slice_Normal_x = normal[0]
        self.state.Slice_Normal_y = normal[1]
        self.state.Slice_Normal_z = normal[2]
        self.state.Slice_Origin_x = origin[0]
        self.state.Slice_Origin_y = origin[1]
        self.state.Slice_Origin_z = origin[2]
        self.state.ST_Default_Point1, self.state.ST_Default_Point2 = self.default_point1_and_point2(normal, origin)

        self.state.ST_Vectors = self.Vectors
        self.state.ST_IntegrationDirection = self.IntegrationDirection
        self.state.ST_IntegratorType = self.IntegratorType
        self.state.ST_MSL = self.MSL
        self.state.ST_MSL_value = self.MSL_value
        self.state.ST_DiagLength = self.DiagLength
        self.state.ST_Resolution = self.Resolution
        self.state.ST_Point1_x = self.Point1_x
        self.state.ST_Point1_y = self.Point1_y
        self.state.ST_Point1_z = self.Point1_z
        self.state.ST_Point2_x = self.Point2_x
        self.state.ST_Point2_y = self.Point2_y
        self.state.ST_Point2_z = self.Point2_z

        print("stream_son read")

    def default_point1_and_point2(self, normal, origin):
        cnt = sum(1 for i in normal if i < 10e-6)
        if cnt == 2:
            if normal[0] == 1:
                return (origin[0], self.state.data_bounds[2], self.state.data_bounds[4]), (origin[1], self.state.data_bounds[3], self.state.data_bounds[5])
            if normal[1] == 1:
                return (self.state.data_bounds[0], origin[1], self.state.data_bounds[4]), (self.state.data_bounds[1], origin[1], self.state.data_bounds[5])
            if normal[2] == 1:
                return (self.state.data_bounds[0], self.state.data_bounds[2], origin[2]), (self.state.data_bounds[1], self.state.data_bounds[3], origin[2])

        return (self.state.data_bounds[0], self.state.data_bounds[2], self.state.data_bounds[4]), (self.state.data_bounds[1], self.state.data_bounds[3], self.state.data_bounds[5])

    def get_module_name(self) -> str:
        return super().get_module_name()

    def rename_module(self, new_name: str):
        super().rename_module(new_name)