from typing import Dict

from trame_server import Server

from Components.Drawer.UICardManager.DataHolder.Data.Data import Data


class GlyphData(Data):
    def __init__(self, data_id: int, name: str, server: Server, slice_data: Data):
        super().__init__(data_id=data_id, name=name, server=server)
        self.slice_data = slice_data
        self.GlyphType = self.state.Glyph_GlyphType_List[0]
        self.OrientationArray = self.state.Glyph_OrientationArray_List[1] \
            if len(self.state.Glyph_OrientationArray_List) else self.state.Glyph_OrientationArray_List[0]
        self.ScaleArray = self.state.Glyph_ScaleArray_List[1] \
            if self.state.Glyph_ScaleArray_List else self.state.Glyph_ScaleArray_List[0]
        self.VectorScaleMode = self.state.Glyph_VectorScaleMode_List[0]
        self.ScaleFactor = self.calculate_default_scale_factor()
        self.CurScaleFactor = 0.01

    def write_in(self):
        print("glyph_son write")
        self.GlyphType = self.state.Glyph_GlyphType
        self.OrientationArray = self.state.Glyph_OrientationArray
        self.ScaleArray = self.state.Glyph_ScaleArray
        self.VectorScaleMode = self.state.Glyph_VectorScaleMode
        self.ScaleFactor = self.state.Glyph_ScaleFactor
        self.CurScaleFactor = self.state.Glyph_CurScaleFactor

    def read_out(self):
        print("glyph_son read")
        super().read_out()
        self.state.Glyph_GlyphType = self.GlyphType
        self.state.Glyph_OrientationArray = self.OrientationArray
        self.state.Glyph_ScaleArray = self.ScaleArray
        self.state.Glyph_VectorScaleMode = self.VectorScaleMode
        self.state.Glyph_ScaleFactor = self.ScaleFactor
        self.state.Glyph_CurScaleFactor = self.CurScaleFactor

    def calculate_default_scale_factor(self) -> Dict[str, float]:
        default_scale_factor = {}
        for pd in self.state.point_data_fields:
            default_scale_factor[pd] = round(0.01 / self.state.point_data_range[pd][1], 7) if self.state.point_data_range[pd][1] != 0 else 0.01
        print("default_scale_factor ", default_scale_factor)
        return default_scale_factor

    def get_module_name(self) -> str:
        return super().get_module_name()

    def rename_module(self, new_name: str):
        super().rename_module(new_name)