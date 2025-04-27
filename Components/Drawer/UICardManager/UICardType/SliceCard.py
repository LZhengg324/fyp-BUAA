from copy import deepcopy
from logging import disable

from trame_server import Server

from Components.Drawer.UICardManager.DataHolder.DataHolder import DataHolder
from Constants.card_type import CardType
from Constants.slice_type import SliceType
from Source.SourceManager import SourceManager
from Source.VisibleManager import VisibleManager
from Components.Drawer.UICardManager.UICard import UICard
from trame.widgets import vuetify3 as vuetify

class SliceCard:
    def __init__(self, card_name: str, server: Server, source_manager: SourceManager,
                 visible_manager: VisibleManager, data_holder: DataHolder):
        self.card_name = card_name
        self.source_manager = source_manager
        self.visible_manager = visible_manager
        self.data_holder = data_holder
        self.server = server
        self.state = server.state
        self.ctrl = server.controller
        self.state.nt_available_delete = False
        self.state.Slice_Origin_x = 0.0
        self.state.Slice_Origin_y = 0.0
        self.state.Slice_Origin_z = 0.0
        self.state.Slice_Normal_x = 1
        self.state.Slice_Normal_y = 0
        self.state.Slice_Normal_z = 0

        # -----------------------------------------------------------------------------
        # Register Callbacks
        # -----------------------------------------------------------------------------

        self.ctrl.x_normal = self.x_normal
        self.ctrl.y_normal = self.y_normal
        self.ctrl.z_normal = self.z_normal
        self.ctrl.create_contour_view = self.create_contour_view
        self.ctrl.modify_slice_props = self.modify_slice_props
        self.ctrl.create_glyph_view = self.create_glyph_view
        self.ctrl.create_stream_tracer_view = self.create_stream_tracer_view
        self.ctrl.reset_props = self.reset_props
        self.ctrl.delete_module = self.delete_module

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------
    def show_card(self):
        with UICard(card_type=CardType.Slice, data_holder=self.data_holder).ui_card() as ui:
            with vuetify.VRow(
            ):
                with vuetify.VCol(cols=4):
                    vuetify.VBtn(
                        text="APPLY",
                        click=self.ctrl.modify_slice_props,
                        variant="tonal",
                        density="comfortable",
                        classes="mx-2",
                        hide_details=True,
                    )
                with vuetify.VCol(
                        cols=4
                ):
                    vuetify.VBtn(
                        text="RESET",
                        click=self.ctrl.reset_props,
                        variant="tonal",
                        density="comfortable",
                        classes="mx-2",
                        hide_details=True,
                    )
                with vuetify.VCol(
                        cols=4
                ):
                    vuetify.VBtn(
                        text="DELETE",
                        click=self.ctrl.delete_module,
                        variant="tonal",
                        density="comfortable",
                        classes="mx-2",
                        disabled=("nt_available_delete", ),
                        hide_details=True,
                    )
            with vuetify.VRow():
                with vuetify.VCol():
                    vuetify.VSelect(
                        hide_details=True,
                        label="Slice Type",
                        v_model=("slice_type", SliceType.Plane),
                        items=("slice_type_list", [
                            {"title": "Plane", "value": SliceType.Plane},
                            # {"title": "Box", "value": SliceType.Box},
                            # {"title": "Cylinder", "value": SliceType.Cylinder},
                            # {"title": "Sphere", "value": SliceType.Sphere},
                        ]),
                        variant="outlined",

                    )
            vuetify.VDivider(
                classes="my-2"
            )
            vuetify.VLabel(
                text="Slice Origin",
                classes="my-1",
            )
            with vuetify.VRow():
                with vuetify.VCol(cols=4):
                    vuetify.VTextField(
                        label="x",
                        v_model=("Slice_Origin_x",),
                        hide_details=True,
                        variant="outlined",
                    )
                with vuetify.VCol(cols=4):
                    vuetify.VTextField(
                        label="y",
                        v_model=("Slice_Origin_y",),
                        hide_details=True,
                        variant="outlined",
                    )
                with vuetify.VCol(cols=4):
                    vuetify.VTextField(
                        label="z",
                        v_model=("Slice_Origin_z",),
                        hide_details=True,
                        variant="outlined",
                    )
            vuetify.VLabel(
                text="Slice Normal",
                classes="my-3",
            )
            with vuetify.VRow():
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VTextField(
                        label="x",
                        v_model=("Slice_Normal_x",),
                        variant="outlined",
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VTextField(
                        label="y",
                        v_model=("Slice_Normal_y",),
                        variant="outlined",
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VTextField(
                        label="z",
                        v_model=("Slice_Normal_z",),
                        variant="outlined",
                        hide_details=True,
                    )
            with vuetify.VRow():
                with vuetify.VCol(
                        cols=4
                ):
                    vuetify.VBtn(
                        text="X Normal",
                        click=self.ctrl.x_normal,
                        style="font-size: 12px",
                    )
                with vuetify.VCol(
                        cols=4
                ):
                    vuetify.VBtn(
                        text="Y Normal",
                        click=self.ctrl.y_normal,
                        style="font-size: 12px",
                    )
                with vuetify.VCol(
                        cols=4
                ):
                    vuetify.VBtn(
                        text="Z Normal",
                        click=self.ctrl.z_normal,
                        style="font-size: 12px",
                    )
            vuetify.VDivider(
                classes="my-2"
            )
            vuetify.VLabel(
                text="Add a View",
                classes="my-3",
            )
            with vuetify.VRow():
                vuetify.VBtn(
                    text="Contour",
                    width="100%",
                    click=self.ctrl.create_contour_view,
                    classes="my-3",
                )
            with vuetify.VRow():
                vuetify.VBtn(
                    text="Glyph",
                    width="100%",
                    click=self.ctrl.create_glyph_view,
                    classes="my-3",
                )
            with vuetify.VRow():
                vuetify.VBtn(
                    text="Stream Trace",
                    width="100%",
                    click=self.ctrl.create_stream_tracer_view,
                    classes="my-3",
                )
            with vuetify.VRow():
                vuetify.VBtn(
                    "Threshold",
                    classes="my-3",
                    width="100%",
                    click=self.ctrl.create_threshold_view,
                )

    # -----------------------------------------------------------------------------
    # GUI Callbacks
    # -----------------------------------------------------------------------------

    def x_normal(self):
        print("used x_normal")
        self.state.Slice_Normal_x = 1
        self.state.Slice_Normal_y = 0
        self.state.Slice_Normal_z = 0

    def y_normal(self):
        print("used y_normal")
        self.state.Slice_Normal_x = 0
        self.state.Slice_Normal_y = 1
        self.state.Slice_Normal_z = 0

    def z_normal(self):
        print("used z_normal")
        self.state.Slice_Normal_x = 0
        self.state.Slice_Normal_y = 0
        self.state.Slice_Normal_z = 1

    def modify_slice_props(self):
        self.source_manager.modify_slice_props(source_id=self.state.active_view,
                                               origin=list(map(float,
                                                               [self.state.Slice_Origin_x, self.state.Slice_Origin_y,
                                                                self.state.Slice_Origin_z])),
                                               normal=list(map(float,
                                                               [self.state.Slice_Normal_x, self.state.Slice_Normal_y,
                                                                self.state.Slice_Normal_z])))
        self.data_holder.write_in(self.state.active_view)
        self.visible_manager.update_view()

    def create_contour_view(self):
        new_view_id = self.source_manager.add_contour(source_id=self.state.active_view)
        self.state.pipeline = (self.state.pipeline
                               + [{"id": str(new_view_id), "parent": str(self.state.active_view),
                                   "visible": 0, "name": "Contour", "type": CardType.Contour}, ])
        self.data_holder.register(name="Contour", source_id=new_view_id, card_type=CardType.Contour,
                                  parent_idx=self.state.active_view)
        self.state.nt_available_delete = True

    def create_glyph_view(self):
        new_view_id = self.source_manager.add_glyph(source_id=self.state.active_view)
        self.state.pipeline = (self.state.pipeline + [{"id": str(new_view_id), "parent": str(self.state.active_view),
                                   "visible": 0, "name": "Glyph", "type": CardType.Glyph}, ])
        self.data_holder.register(name="Glyph", source_id=new_view_id, card_type=CardType.Glyph,
                                  parent_idx=self.state.active_view)
        self.state.nt_available_delete = True

    def create_stream_tracer_view(self):
        new_view_id = self.source_manager.add_stream_tracer(source_id=self.state.active_view)
        self.state.pipeline = (self.state.pipeline + [{"id": str(new_view_id), "parent": str(self.state.active_view),
                                                       "visible": 0, "name": "StreamTracer", "type": CardType.StreamTracer}, ])
        self.data_holder.register(name="StreamTracer", source_id=new_view_id, card_type=CardType.StreamTracer,
                                  parent_idx=self.state.active_view)
        self.state.nt_available_delete = True

    def reset_props(self):
        self.data_holder.get_data(self.state.active_view).read_out()

    def delete_module(self):
        # Data Holder
        self.data_holder.delete_module(self.state.active_view)

        # Visible Manager
        self.visible_manager.set_visible(self.state.active_view, False)

        # Source Manager
        self.source_manager.delete_module(self.state.active_view)

        # Pipeline Widget
        t = deepcopy(self.state.pipeline)
        for idx, item in enumerate(t):
            if item["id"] == str(self.state.active_view):
                t.pop(idx)
                self.state.pipeline = t
                break
        self.state.active_ui = None
        self.state.active_view = 0
