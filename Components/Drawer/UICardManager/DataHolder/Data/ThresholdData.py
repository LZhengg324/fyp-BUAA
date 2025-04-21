from typing import Tuple

from trame_server import Server

from Components.Drawer.UICardManager.DataHolder.Data.Data import Data


class ThresholdData(Data):
    def __init__(self, data_id: int, name: str, server: Server):
        super().__init__(data_id=data_id, name=name, server=server)
        self.Threshold_sel_scalar = self.state.scalar_fields[0]
        self.Threshold_lower_value = self.state.point_data_range[self.state.Threshold_sel_scalar][0]
        self.Threshold_upper_value = self.state.point_data_range[self.state.Threshold_sel_scalar][1]
        self.Threshold_method = self.state.Threshold_method_list[0]
        self.Threshold_AllScalars = True
        self.Threshold_UseContinuousCellRange = False
        self.Threshold_Invert = False

    def write_in(self):
        print("threshold_son write")
        self.Threshold_sel_scalar = self.state.Threshold_sel_scalar
        self.Threshold_lower_value = self.state.Threshold_lower_value
        self.Threshold_upper_value = self.state.Threshold_upper_value
        self.Threshold_method = self.state.Threshold_method
        self.Threshold_AllScalars = self.state.Threshold_AllScalars
        self.Threshold_UseContinuousCellRange = self.state.Threshold_UseContinuousCellRange
        self.Threshold_Invert = self.state.Threshold_Invert

    def read_out(self):
        print("threshold_son read")
        super().read_out()
        self.state.Threshold_sel_scalar = self.Threshold_sel_scalar
        self.state.Threshold_lower_value = self.Threshold_lower_value
        self.state.Threshold_upper_value = self.Threshold_upper_value
        self.state.Threshold_method = self.Threshold_method
        self.state.Threshold_AllScalars = self.Threshold_AllScalars
        self.state.Threshold_UseContinuousCellRange = self.Threshold_UseContinuousCellRange
        self.state.Threshold_Invert = self.Threshold_Invert
        pass

    def get_module_name(self) -> str:
        return super().get_module_name()

    def rename_module(self, new_name: str):
        super().rename_module(new_name)