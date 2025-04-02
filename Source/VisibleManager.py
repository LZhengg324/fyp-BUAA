import paraview.web.venv  # Available in PV 5.10

from trame_server import Server
from trame.widgets import paraview as pv

from Constants.card_type import CardType
from Source.SourceManager import SourceManager
from paraview import simple

class VisibleManager:
    def __init__(self, server: Server, source_manager: SourceManager, render_view):
        self.LookupTable = {}
        self.server = server
        self.visible_items = {}
        self.source_manager = source_manager
        self.render_view = render_view
        self.state = server.state
        self.ctrl = server.controller

    def initialize_lookup_table(self, main_block_id: int):
        main_source = self.source_manager.get_source(main_block_id, self.state.cur_step)
        for point_data in self.state.point_data_fields:
            display = simple.Show(main_source, self.render_view)
            simple.ColorBy(display, ("POINTS", point_data))
            self.LookupTable[point_data] = display.LookupTable
            simple.Delete(display)


    def set_visible(self, vid: int, visible: bool):
        if visible:
            self.visible_items[vid] = self.get_display(vid=vid)
        else:
            if vid in self.visible_items.keys():
                display = self.visible_items[vid]
                simple.Delete(display)
                self.visible_items.pop(vid)
        simple.Render(self.render_view)
        # self.render_view.ResetCamera()
        self.ctrl.view_update()
        # self.render_view.ResetCamera()

    def update_view(self):
        for display in self.visible_items.values():
            simple.Delete(display)
        for key in self.visible_items.keys():
            self.visible_items[key] = self.get_display(key)
        simple.Render(self.render_view)
        # self.render_view.ResetCamera()
        self.ctrl.view_update()

    def mesh_or_point_data_update(self):
        for vid, display in self.visible_items.items():
            display.LookupTable = self.LookupTable[self.state.cur_point_data]
            display.ColorArrayName = (self.state.cur_mesh, self.state.cur_point_data)
        simple.Render(self.render_view)
        # self.render_view.ResetCamera()
        self.ctrl.view_update()

    def get_render_view(self):
        return self.render_view

    def get_display(self, vid: int):
        display = simple.Show(self.source_manager.get_source(vid, self.state.cur_step), self.render_view)
        display.LookupTable = self.LookupTable[self.state.cur_point_data]
        display.ColorArrayName = (self.state.cur_mesh, self.state.cur_point_data)
        return display

    def reboot_all_for_new_main_module(self):
        for display in self.visible_items.values():
            simple.Delete(display)
        self.visible_items.clear()
        print("visible manager", self.visible_items)
