from trame_server import Server

from Components.Drawer.UICardManager.DataHolder import DataHolder
from Constants.card_type import CardType
from Source.SourceManager import SourceManager
from Source.VisibleManager import VisibleManager
from Components.Drawer.UICardManager.UICard import UICard
from trame.widgets import vuetify3 as vuetify

class GlyphCard:
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

        # List
        self.state.Glyph_GlyphType_List = ["Arrow", "Cone", "Box", "Cylinder", "Line", "Sphere", "2dGlyph"]
        self.state.Glyph_OrientationArray_List = ["No Orientation Array"] + self.state.vector_field
        self.state.Glyph_ScaleArray_List = ["No Scale Array"] + self.state.point_data_fields
        self.state.Glyph_VectorScaleMode_List = ["Scale by Magnitude", "Scale by Components"]

        # Variable
        self.state.Glyph_GlyphType = self.state.Glyph_GlyphType_List[0]
        self.state.Glyph_OrientationArray = ""
        self.state.Glyph_ScaleArray = ""
        self.state.Glyph_VectorScaleMode = self.state.Glyph_VectorScaleMode_List[0]
        self.state.Glyph_ScaleFactor = ""
        self.state.Glyph_CurScaleFactor = 0.01
        self.state.Glyph_show_vector_scale_mode = False

        @self.state.change('vector_field')
        def update_vector_field(vector_field, **kwargs):
            self.state.Glyph_OrientationArray_List = ["No Orientation Array"] + self.state.vector_field

        @self.state.change('point_data_fields')
        def update_point_data_fields(point_data_fields, **kwargs):
            self.state.Glyph_ScaleArray_List = ["No Scale Array"] + self.state.point_data_fields

        # -----------------------------------------------------------------------------
        # CallBacks Register
        # -----------------------------------------------------------------------------

        self.ctrl.modify_glyph_props = self.modify_glyph_props
        self.ctrl.reset_default_value = self.reset_default_value

        # -----------------------------------------------------------------------------
        # State CallBacks
        # -----------------------------------------------------------------------------

        @self.state.change('Glyph_ScaleArray')
        def update_Glyph_ScaleArray(Glyph_ScaleArray, **kwargs):
            if Glyph_ScaleArray in self.state.scalar_fields:
                self.state.Glyph_show_vector_scale_mode = False
                self.state.Glyph_VectorScaleMode = "Scale by Magnitude"
            else:
                self.state.Glyph_show_vector_scale_mode = True

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------
    def show_card(self):
        with UICard(card_type=CardType.Glyph, data_holder=self.data_holder).ui_card() as ui:
            with vuetify.VRow(
            ):
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VBtn(
                        "APPLY",
                        click=self.ctrl.modify_glyph_props,
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
                        hide_details=True,
                    )
            vuetify.VLabel(
                "Glyph Source",
                classes="my-5 font-weight-bold",
            )
            with vuetify.VRow():
                vuetify.VSelect(
                    label="Glyph Type",
                    v_model=("Glyph_GlyphType",),
                    items=("Glyph_GlyphType_List", ),
                    classes="my-2",
                    variant="outlined",
                )
            vuetify.VLabel(
                "Orientation",
                classes="my-3 font-weight-bold",
            )
            vuetify.VDivider(
                classes="mb-5",
            )
            with vuetify.VRow():
                vuetify.VSelect(
                    label="Orientation Array",
                    v_model=("Glyph_OrientationArray",),
                    items=("Glyph_OrientationArray_List", ),
                    variant="outlined",
                    classes="my-2",
                )
            vuetify.VLabel(
                "Scale",
                classes="my-3 font-weight-bold",
            )
            with vuetify.VRow():
                vuetify.VSelect(
                    label="Scale Array",
                    v_model=("Glyph_ScaleArray",),
                    items=("Glyph_ScaleArray_List", ),
                    classes="my-2",
                    variant="outlined",
                )
            with vuetify.VRow():
                vuetify.VSelect(
                    label="Vector Scale Mode",
                    v_model=("Glyph_VectorScaleMode",),
                    items=("Glyph_VectorScaleMode_List", ),
                    classes="my-2",
                    v_show=("Glyph_show_vector_scale_mode",),
                    variant="outlined",
                )
            vuetify.VLabel(
                label="Scale Factor",
                classes="my-2",
            )
            with vuetify.VRow():
                with vuetify.VCol(
                    cols=9
                ):
                    vuetify.VSlider(
                        v_model=("Glyph_CurScaleFactor","Glyph_ScaleFactor[Glyph_ScaleArray]"),
                        min=0,
                        max=0.01,
                        step=0.0001,
                        # classes="my-2"
                    )
                with vuetify.VCol(
                    cols=3
                ):
                    vuetify.VBtn(
                        icon="mdi mdi-autorenew",
                        click=self.ctrl.reset_default_value,
                    )
            vuetify.VLabel(
                "{{Glyph_CurScaleFactor}}"
            )


    def reset_default_value(self):
        if self.state.Glyph_ScaleArray == "No Scale Array":
            self.state.Glyph_CurScaleFactor = 0.01
            return
        self.state.Glyph_CurScaleFactor = round(0.01 / self.state.point_data_range[self.state.Glyph_ScaleArray][1], 7)

    def modify_glyph_props(self):
        print("modify_glyph_props")
        self.source_manager.modify_glyph_props(source_id=self.state.active_view,
                                               glyph_type=self.state.Glyph_GlyphType,
                                               orientation_array=self.state.Glyph_OrientationArray,
                                               scale_array=self.state.Glyph_ScaleArray,
                                               vector_scale_mode=self.state.Glyph_VectorScaleMode,
                                               scale_factor=self.state.Glyph_CurScaleFactor, )
        self.data_holder.write_in(self.state.active_view)
        self.visible_manager.update_view()


# class GlyphType:
#     Arrow = 1
#     Cone = 2
#     Box = 3
#     Cylinder = 4
#     Line = 5
#     Sphere = 6
#     twoDGlyph = 7