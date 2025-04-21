from copy import deepcopy
from math import sqrt

from trame_server import Server

from Components.Drawer.UICardManager.DataHolder import DataHolder
from Constants.card_type import CardType
from Source.SourceManager import SourceManager
from Source.VisibleManager import VisibleManager
from Components.Drawer.UICardManager.UICard import UICard
from trame.widgets import vuetify3 as vuetify

class StreamTracerCard:
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
        self.state.ST_IntegrationDirection_List = ["FORWARD", "BACKWARD", "BOTH"]
        self.state.ST_IntegratorType_List = ["Runge-Kutta 2", "Runge-Kutta 4", "Runge-Kutta 4-5"]

        # Variable
        self.state.ST_Vectors = self.state.vector_field[0] if self.state.vector_field else None
        self.state.ST_IntegrationDirection = self.state.ST_IntegrationDirection_List[-1]
        self.state.ST_IntegratorType = self.state.ST_IntegratorType_List[-1]
        self.state.ST_MSL = max(self.state.data_bounds[i] for i in range(1, len(self.state.data_bounds), 2))
        self.state.ST_MSL_value = self.state.ST_MSL
        self.state.ST_DiagLength = sqrt(sum((self.state.data_bounds[i] - self.state.data_bounds[i - 1]) ** 2
                                            for i in range(1, len(self.state.data_bounds), 2)))
        self.state.ST_Resolution = 1000
        self.state.ST_Point1_x = 0
        self.state.ST_Point1_y = 0
        self.state.ST_Point1_z = 0
        self.state.ST_Point2_x = self.state.data_bounds[1]
        self.state.ST_Point2_y = self.state.data_bounds[3]
        self.state.ST_Point2_z = self.state.data_bounds[5]

        # -----------------------------------------------------------------------------
        # CallBacks Register
        # -----------------------------------------------------------------------------

        self.ctrl.reset_default_MSL = self.reset_default_MSL
        self.ctrl.click_x_axis = self.click_x_axis
        self.ctrl.click_y_axis = self.click_y_axis
        self.ctrl.click_z_axis = self.click_z_axis
        self.ctrl.click_center_on_bounds = self.click_center_on_bounds
        self.ctrl.modify_stream_tracer_props = self.modify_stream_tracer_props

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------
    def show_card(self):
        with UICard(card_type=CardType.StreamTracer, data_holder=self.data_holder).ui_card() as ui:
            with vuetify.VRow(
            ):
                with vuetify.VCol(cols=4):
                    vuetify.VBtn(
                        "APPLY",
                        click=self.ctrl.modify_stream_tracer_props,
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
            with vuetify.VRow(
                align="center",
            ):
                with vuetify.VCol(
                    cols=3,
                    align_self="center"
                ):
                    vuetify.VLabel(
                        "Vector",
                        classes="my-2",
                    )
                with vuetify.VCol(
                    cols=9
                ):
                    vuetify.VSelect(
                        variant="outlined",
                        v_model=("ST_Vectors",),
                        items=("vector_field",),
                        hide_details=True,
                    )
            vuetify.VLabel(
                "Integration Parameters",
                classes="my-2 font-weight-bold",
            )
            vuetify.VDivider(
                classes="my-2"
            )
            with vuetify.VRow(
                classes="my-2"
            ):
                vuetify.VSelect(
                    label="Integration Direction",
                    v_model=("ST_IntegrationDirection",),
                    items=("ST_IntegrationDirection_List",),
                    variant="outlined",
                    classes = "my-2",
                    hide_details=True,
                )
            with vuetify.VRow(
                classes="my-2"
            ):
                vuetify.VSelect(
                    label="Integrator Type",
                    v_model=("ST_IntegratorType",),
                    items=("ST_IntegratorType_List",),
                    variant="outlined",
                    classes="my-2",
                    hide_details=True,
                )
            vuetify.VLabel(
                "Streamline Parameters",
                classes="my-2 font-weight-bold",
            )
            vuetify.VDivider(
                classes="my-2"
            )
            vuetify.VLabel(
                "Maximum Streamline Length",
                classes="my-2",
            )
            with vuetify.VRow():
                with vuetify.VCol(
                    cols=6,
                    align_self="center"
                ):
                    vuetify.VSlider(
                        min=0,
                        max=("ST_MSL",),
                        step=0.001,
                        v_model=("ST_MSL_value",),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=4,
                    align_self="center"
                ):
                    vuetify.VTextField(
                        variant="outlined",
                        v_model=("ST_MSL_value", "ST_MSL_value"),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=2,
                    align_self="center"
                ):
                    vuetify.VIcon(
                        icon="mdi mdi-autorenew",
                        click=self.ctrl.reset_default_MSL,
                    )
            vuetify.VLabel(
                "Seeds",
                classes="my-2 font-weight-bold",
            )
            vuetify.VDivider(
                classes="my-2"
            )
            with vuetify.VRow():
                with vuetify.VCol(
                    cols=3,
                    align_self="center",
                ):
                    vuetify.VLabel(
                        "Seed Type",
                        style="font-size: 12px",
                    )
                with vuetify.VCol(
                    cols=9,
                    align_self="center"
                ):
                    vuetify.VTextField(
                        "Line",
                        variant="outlined",
                        disabled=True,
                        hide_details=True,
                    )
            with vuetify.VRow():
                vuetify.VLabel(
                    "Line Parameters",
                    classes="mx-2 my-2 font-weight-bold",
                )
            vuetify.VDivider(
                classes="my-2"
            )
            with vuetify.VRow():
                vuetify.VLabel(
                    "Length: {{ ST_DiagLength }}",
                    classes="mx-2 my-2 font-weight-bold",
                )
            with vuetify.VRow():
                vuetify.VLabel(
                    "Point1",
                    classes="mx-2"
                )
            with vuetify.VRow():
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VTextField(
                        label="x",
                        v_model=("ST_Point1_x", ),
                        variant="outlined",
                        hide_details=True,
                    )
                with vuetify.VCol(
                        cols=4
                ):
                    vuetify.VTextField(
                        label="y",
                        v_model=("ST_Point1_y",),
                        variant="outlined",
                        hide_details=True,
                    )
                with vuetify.VCol(
                        cols=4
                ):
                    vuetify.VTextField(
                        label="z",
                        v_model=("ST_Point1_z",),
                        variant="outlined",
                        hide_details=True,
                    )
            with vuetify.VRow():
                vuetify.VLabel(
                    "Point2",
                    classes="mx-2"
                )
            with vuetify.VRow(

            ):
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VTextField(
                        label="x",
                        v_model=("ST_Point2_x",),
                        variant="outlined",
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VTextField(
                        label="y",
                        v_model=("ST_Point2_y",),
                        variant="outlined",
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VTextField(
                        label="z",
                        v_model=("ST_Point2_z",),
                        variant="outlined",
                        hide_details=True,
                    )
            with vuetify.VRow(
                classes="my-2",
            ):
                with vuetify.VCol(
                    cols=4,
                ):
                    vuetify.VBtn(
                        "x axis",
                        width="100%",
                        classes="mx-1",
                        click=self.ctrl.click_x_axis,
                    )
                with vuetify.VCol(
                    cols=4,
                ):
                    vuetify.VBtn(
                        "y axis",
                        width="100%",
                        classes="mx-1",
                        click=self.ctrl.click_y_axis,
                    )
                with vuetify.VCol(
                    cols=4,
                ):
                    vuetify.VBtn(
                        "z axis",
                        width="100%",
                        classes="mx-1",
                        click=self.ctrl.click_z_axis,
                    )
            with vuetify.VRow(
                classes="my-2",
                align="center",
                justify="center",
            ):
                vuetify.VBtn(
                    "Center on bounds",
                    width="100%",
                    click=self.ctrl.click_center_on_bounds,
                )
            with vuetify.VRow():
                vuetify.VTextField(
                    label="Resolution",
                    v_model=("ST_Resolution", ),
                    variant="outlined",
                    classes="my-2",
                    # v_on={"@keypress.native.enter": "modify_stream_tracer_props"}
                )
            with vuetify.VRow():
                vuetify.VBtn(
                    "Threshold",
                    classes="my-3",
                    width="100%",
                    click=self.ctrl.create_threshold_view,
                )

    # ----------------------------------------------------------------------------
    # GUI Callbacks
    # ----------------------------------------------------------------------------

    def reset_default_MSL(self):
        self.state.ST_MSL_value = self.state.ST_MSL

    def click_x_axis(self):
        self.state.ST_Point1_x = self.state.data_bounds[0]
        self.state.ST_Point1_y = self.state.Slice_Origin_y
        self.state.ST_Point1_z = self.state.Slice_Origin_z
        self.state.ST_Point2_x = self.state.data_bounds[1]
        self.state.ST_Point2_y = self.state.Slice_Origin_y
        self.state.ST_Point2_z = self.state.Slice_Origin_z

    def click_y_axis(self):
        self.state.ST_Point1_x = self.state.Slice_Origin_x
        self.state.ST_Point1_y = self.state.data_bounds[2]
        self.state.ST_Point1_z = self.state.Slice_Origin_z
        self.state.ST_Point2_x = self.state.Slice_Origin_x
        self.state.ST_Point2_y = self.state.data_bounds[3]
        self.state.ST_Point2_z = self.state.Slice_Origin_z

    def click_z_axis(self):
        self.state.ST_Point1_x = self.state.Slice_Origin_x
        self.state.ST_Point1_y = self.state.Slice_Origin_y
        self.state.ST_Point1_z = self.state.data_bounds[4]
        self.state.ST_Point2_x = self.state.Slice_Origin_x
        self.state.ST_Point2_y = self.state.Slice_Origin_y
        self.state.ST_Point2_z = self.state.data_bounds[5]

    def click_center_on_bounds(self):
        self.state.ST_Point1_x, self.state.ST_Point1_y, self.state.ST_Point1_z = deepcopy(self.state.ST_Default_Point1)
        self.state.ST_Point2_x, self.state.ST_Point2_y, self.state.ST_Point2_z = deepcopy(self.state.ST_Default_Point2)

    def modify_stream_tracer_props(self):
        print("modify_st_props")
        self.source_manager.modify_stream_tracer_props(source_id=self.state.active_view,
                                                       vector=self.state.ST_Vectors,
                                                       integration_direction=self.state.ST_IntegrationDirection,
                                                       integrator_type=self.state.ST_IntegratorType,
                                                       msl_value=self.state.ST_MSL_value,
                                                       resolution=int(self.state.ST_Resolution),
                                                       point1_x=float(self.state.ST_Point1_x),
                                                       point1_y=float(self.state.ST_Point1_y),
                                                       point1_z=float(self.state.ST_Point1_z),
                                                       point2_x=float(self.state.ST_Point2_x),
                                                       point2_y=float(self.state.ST_Point2_y),
                                                       point2_z=float(self.state.ST_Point2_z), )
        self.data_holder.write_in(self.state.active_view)
        self.visible_manager.update_view()