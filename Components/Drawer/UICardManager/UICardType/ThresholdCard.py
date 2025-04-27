from trame_server import Server

from Components.Drawer.UICardManager.DataHolder import DataHolder
from Constants.card_type import CardType
from Source.SourceManager import SourceManager
from Source.VisibleManager import VisibleManager
from Components.Drawer.UICardManager.UICard import UICard
from trame.widgets import vuetify3 as vuetify

class ThresholdCard:
    def __init__(self, card_name: str, server: Server, source_manager: SourceManager,
                 visible_manager: VisibleManager, data_holder: DataHolder):
        self.card_name = card_name
        self.source_manager = source_manager
        self.visible_manager = visible_manager
        self.data_holder = data_holder
        self.server = server
        self.state = server.state
        self.ctrl = server.controller

        # List
        self.state.Threshold_value_step = {}
        self.state.Threshold_method_list = ["Between", "Below Lower Threshold", "Above Upper Threshold"]

        # Variable
        self.state.Threshold_sel_scalar = ""
        self.state.Threshold_lower_value = 0
        self.state.Threshold_upper_value = 0
        self.state.Threshold_method = self.state.Threshold_method_list[0]
        self.state.Threshold_AllScalars = True
        self.state.Threshold_UseContinuousCellRange = False
        self.state.Threshold_Invert = False

        # -----------------------------------------------------------------------------
        # CallBacks Register
        # -----------------------------------------------------------------------------

        self.ctrl.modify_threshold_props = self.modify_threshold_props
        self.ctrl.default_lower_value = self.default_lower_value
        self.ctrl.default_upper_value = self.default_upper_value

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------
    def show_card(self):
        with UICard(card_type=CardType.Threshold, data_holder=self.data_holder).ui_card() as ui:
            with vuetify.VRow(
            ):
                with vuetify.VCol(cols=4):
                    vuetify.VBtn(
                        "APPLY",
                        click=self.ctrl.modify_threshold_props,
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
                        "Scalar",
                        classes="my-2",
                    )
                with vuetify.VCol(
                        cols=9
                ):
                    vuetify.VSelect(
                        variant="outlined",
                        v_model=("Threshold_sel_scalar",),
                        items=("scalar_fields",),
                        hide_details=True,
                    )
            vuetify.VDivider(
                classes="my-2"
            )
            vuetify.VLabel(
                "Lower Threshold",
                classes="my-4",
                v_show=f"Threshold_method == 'Between' || Threshold_method == 'Below Lower Threshold'",
            )
            with vuetify.VRow(
                v_show=f"Threshold_method == 'Between' || Threshold_method == 'Below Lower Threshold'",
            ):
                with vuetify.VCol(
                    cols=6,
                    align_self="center"
                ):
                    vuetify.VSlider(
                        min=("point_data_range[Threshold_sel_scalar][0]",),
                        max=("point_data_range[Threshold_sel_scalar][1]",),
                        step=("Threshold_value_step[pd]",),
                        v_model=("Threshold_lower_value",),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=4,
                    align_self="center"
                ):
                    vuetify.VTextField(
                        variant="outlined",
                        v_model=("Threshold_lower_value", "Threshold_lower_value"),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=2,
                    align_self="center"
                ):
                    vuetify.VIcon(
                        icon="mdi mdi-autorenew",
                        click=self.ctrl.default_lower_value,
                    )
            vuetify.VLabel(
                "Upper Threshold",
                classes="my-4",
                v_show=f"Threshold_method == 'Between' || Threshold_method == 'Above Upper Threshold'",
            )
            with vuetify.VRow(
                v_show=f"Threshold_method == 'Between' || Threshold_method == 'Above Upper Threshold'",
            ):
                with vuetify.VCol(
                    cols=6,
                    align_self="center"
                ):
                    vuetify.VSlider(
                        min=("point_data_range[Threshold_sel_scalar][0]",),
                        max=("point_data_range[Threshold_sel_scalar][1]",),
                        step=("Threshold_value_step[pd]",),
                        v_model=("Threshold_upper_value",),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=4,
                    align_self="center"
                ):
                    vuetify.VTextField(
                        variant="outlined",
                        v_model=("Threshold_upper_value", "Threshold_upper_value"),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=2,
                    align_self="center"
                ):
                    vuetify.VIcon(
                        icon="mdi mdi-autorenew",
                        click=self.ctrl.default_upper_value,
                    )
            with vuetify.VRow():
                vuetify.VSelect(
                    label="Threshold Method",
                    v_model=("Threshold_method",),
                    items=("Threshold_method_list",),
                    variant="outlined",
                    classes="my-2",
                    width="100%",
                    hide_details=True,
                )
            with vuetify.VRow(
                no_gutters=True,
                classes="mt-2 mb-0",
                dense=True,
            ):
                with vuetify.VCol(
                    cols=2,
                ):
                    vuetify.VCheckbox(
                        v_model=("Threshold_AllScalars",),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=10,
                    align_self="center"
                ):
                    vuetify.VLabel(
                        "All Scalars",
                    )
            with vuetify.VRow(
                no_gutters=True,
                classes="my-0",
                dense=True,
            ):
                with vuetify.VCol(
                    cols=2
                ):
                    vuetify.VCheckbox(
                        v_model=("Threshold_UseContinuousCellRange",),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=10,
                    align_self="center"
                ):
                    vuetify.VLabel(
                        "Use Continuous Cell Range",
                    )
            with vuetify.VRow(
                no_gutters=True,
                classes="my-0",
                dense=True,
            ):
                with vuetify.VCol(
                    cols=2
                ):
                    vuetify.VCheckbox(
                        v_model=("Threshold_Invert",),
                        hide_details=True,
                    )
                with vuetify.VCol(
                    cols=10,
                    align_self="center"
                ):
                    vuetify.VLabel(
                        "Invert",
                    )

    # ----------------------------------------------------------------------------
    # GUI Callbacks
    # ----------------------------------------------------------------------------

    def modify_threshold_props(self):
        self.source_manager.modify_threshold_props(source_id=self.state.active_view,
                                                   scalar=self.state.Threshold_sel_scalar,
                                                   lower_value=self.state.Threshold_lower_value,
                                                   upper_value=self.state.Threshold_upper_value,
                                                   method=self.state.Threshold_method,
                                                   all_scalars=self.state.Threshold_AllScalars,
                                                   use_continuous_cell_range=self.state.Threshold_UseContinuousCellRange,
                                                   invert=self.state.Threshold_Invert)
        self.data_holder.write_in(self.state.active_view)
        self.visible_manager.update_view()

    def default_lower_value(self):
        self.state.Threshold_lower_value = self.state.point_data_range[self.state.Threshold_sel_scalar][0]

    def default_upper_value(self):
        self.state.Threshold_upper_value = self.state.point_data_range[self.state.Threshold_sel_scalar][1]