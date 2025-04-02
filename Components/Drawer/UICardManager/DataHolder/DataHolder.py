from typing import Dict, Optional, Tuple, Union

from trame_server import Server

from Components.Drawer.UICardManager.DataHolder.Data.Data import Data
from Components.Drawer.UICardManager.DataHolder.Data.MainData import MainData
from Components.Drawer.UICardManager.DataHolder.Data.SliceData import SliceData
from Components.Drawer.UICardManager.DataHolder.Data.ContourData import ContourData
from Components.Drawer.UICardManager.DataHolder.Data.GlyphData import GlyphData
from Components.Drawer.UICardManager.DataHolder.Data.StreamTracerData import StreamTracerData
from Constants.card_type import CardType

class DataHolder:
    def __init__(self, server: Server):
        self.data_cache: Dict[int, Data] = dict()
        self.server = server
        self.state = self.server.state

    def create_data(self, data_id: int, name: str, card_type: CardType,
                    data_bounds: Optional[Tuple[float, float, float, float, float, float]] = None,
                    parent_idx: Optional[int] = None
                    ) -> Union[None, StreamTracerData, GlyphData, SliceData, MainData, ContourData, Data]:
        if card_type == CardType.Main:
            return MainData(data_id=data_id, name=name, server=self.server, data_bounds=data_bounds)
        elif card_type == CardType.Slice:
            sdo = self.get_data(parent_idx).get_slice_default_origin()
            return SliceData(data_id=data_id, name=name, server=self.server, slice_default_origin=sdo)
        elif card_type == CardType.Contour:
            slice_data = self.get_data(parent_idx)
            return ContourData(data_id=data_id, name=name, server=self.server, slice_data=slice_data)
        elif card_type == CardType.Glyph:
            slice_data = self.get_data(parent_idx)
            return GlyphData(data_id=data_id, name=name, server=self.server, slice_data=slice_data)
        elif card_type == CardType.StreamTracer:
            slice_data = self.get_data(parent_idx)
            if isinstance(slice_data, SliceData):
                return StreamTracerData(data_id=data_id, name=name, server=self.server, slice_data=slice_data)
        else:
            return Data(data_id=data_id, name=name, server=self.server)

    def register(self, name: str, source_id: int, card_type: CardType,
                 data_bounds: Optional[Tuple[float, float, float, float, float, float]] = None,
                 parent_idx: Optional[int] = None):

        card_data = self.create_data(data_id=source_id, name=name, card_type=card_type, data_bounds=data_bounds, parent_idx=parent_idx)
        self.data_cache[source_id] = card_data

    def get_data(self, source_id: int):
        return self.data_cache[source_id]

    def read_out(self, source_id: int) -> None:
        self.data_cache[source_id].read_out()

    def write_in(self, source_id: int) -> None:
        self.data_cache[source_id].write_in()

    def delete_module(self, data_id: int):
        self.data_cache.pop(data_id)

    def reboot_all_for_new_main_module(self):
        self.data_cache.clear()
        print("data holder", self.data_cache)