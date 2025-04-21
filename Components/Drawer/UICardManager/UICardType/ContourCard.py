from copy import deepcopy

import numpy as np
from trame_server import Server

from Components.Drawer.UICardManager.DataHolder import DataHolder
from Constants.card_type import CardType
from Source.SourceManager import SourceManager
from Source.VisibleManager import VisibleManager
from Components.Drawer.UICardManager.UICard import UICard
from trame.widgets import vuetify3 as vuetify

class ContourCard:
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
        self.state.Isosurfaces = {}
        self.state.contour_by = self.state.scalar_fields[0]
        self.state.selected_item = []
        self.state.batch_dialog = False
        self.state.linear_num = 10

        @self.state.change('Isosurfaces')
        def update_Isosurfaces(Isosurfaces, **kwargs):
            print("Isosurfaces changed : ", Isosurfaces)
            pass

        @self.state.change('selected_item')
        def update_selected_item(selected_item, **kwargs):
            print(selected_item)

        @self.state.change('contour_by')
        def update_selected_item(contour_by, **kwargs):
            print(contour_by)

        # -----------------------------------------------------------------------------
        # Register Callbacks
        # -----------------------------------------------------------------------------

        self.ctrl.add_contour_value = self.add_contour_value
        self.ctrl.minus_contour_value = self.minus_contour_value
        self.ctrl.modify_contour_props = self.modify_contour_props
        self.ctrl.open_batch_dialog = self.open_batch_dialog
        self.ctrl.close_batch_dialog = self.close_batch_dialog
        self.ctrl.generate_batch_isosurfaces = self.generate_batch_isosurfaces

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------

    def show_card(self):
        with vuetify.VDialog(
            v_model = ("batch_dialog",),
            width="500"
        ):
            with vuetify.VCard():
                vuetify.VCardText(
                    "Range: [{{point_data_range[contour_by][0]}}, "
                    "{{point_data_range[contour_by][1]}}]"
                )
                vuetify.VTextField(
                    label="number",
                    v_model=("linear_num", 0)
                )
                vuetify.VBtn(
                    "Generate",
                    # disabled= ("uploading",),
                    click=self.ctrl.generate_batch_isosurfaces,
                )
        with UICard(card_type=CardType.Contour, data_holder=self.data_holder).ui_card() as ui:
            with vuetify.VRow():
                with vuetify.VCol(
                    cols=4
                ):
                    vuetify.VBtn(
                        "APPLY",
                        click=self.ctrl.modify_contour_props,
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
            with vuetify.VRow():
                vuetify.VSelect(
                    label="Contour By",
                    hide_details=True,
                    v_model=("contour_by", ),
                    items=("scalar_fields",),
                    variant="outlined",
                    classes="my-3",
                )
            vuetify.VLabel(
                text="Isosurfaces",
                classes="mt-3 mb-1",
            )
            with vuetify.VRow():
                with vuetify.VCol(
                  cols=10
                ):
                    vuetify.VList(
                        # v_model=("selected_item", None),  # 选中的项
                        selectable=True,
                        v_model_selected=("selected_item",),
                        select_strategy="single-independent",
                        # items=("list_items", [{"title": "a", "value": 1}, {"title": "b","value": 2}, {"title": "c","value": 3}, {"title": "d","value": 4}, {"title": "e","value": 5}]),
                        items=("Isosurfaces[contour_by]", {}),
                        dense=True,
                        style="height: 200px; border:1px solid #000;",  # 设置高度
                        classes="overflow-y-auto my-3",  # 启用滚动并设置 margin
                        __properties=[
                            ("v_model_selected", "v-model:selected"),
                            "selectable",
                        ],
                    )
            vuetify.VLabel(
                "Range:[{{point_data_range[contour_by][0]}} ,"
                "{{point_data_range[contour_by][1]}}] ",
                style="font-size: 12px",
                classes="my-3",
            )
            with vuetify.VRow():
                vuetify.VTextField(
                    label="value",
                    v_model=("selected_item", ),
                    variant="outlined",
                )
            with vuetify.VRow():
                vuetify.VBtn(
                    icon="mdi-plus",
                    classes="ma-3",
                    click=self.ctrl.add_contour_value,
                )
                vuetify.VBtn(
                    icon="mdi-minus",
                    classes="ma-3",
                    click=self.ctrl.minus_contour_value,
                )
                vuetify.VBtn(
                    icon="mdi-chart-line-variant",
                    classes="ma-3",
                    click=self.ctrl.open_batch_dialog,
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

    def add_contour_value(self):
        print("used add_contour_value")
        t, new_value = self.get_deepcopy_and_target()
        t[self.state.contour_by] = t[self.state.contour_by] + [
            {"title": str(new_value), "value": new_value}, ]
        self.state.Isosurfaces = t

    def minus_contour_value(self):
        print("used minus_contour_value")
        if len(self.state.Isosurfaces[self.state.contour_by]) == 1:
            return
        t, target = self.get_deepcopy_and_target()
        for i in range(len(t[self.state.contour_by]) - 1, -1, -1):
            if t[self.state.contour_by][i]["value"] == target:
                del t[self.state.contour_by][i]
                break
        self.state.Isosurfaces = t

    def get_deepcopy_and_target(self):
        t = deepcopy(self.state.Isosurfaces)
        if type(self.state.selected_item) is list and self.state.selected_item:
            target = self.state.selected_item[0]
        elif self.state.selected_item:
            target = float(self.state.selected_item)
        else:
            target = t[self.state.contour_by][-1]["value"]
        return t, target

    def open_batch_dialog(self):
        self.state.batch_dialog = True

    def close_batch_dialog(self):
        self.state.batch_dialog = False

    def modify_contour_props(self):
        isosurfaces = list(float(self.state.Isosurfaces[self.state.contour_by][i]["value"]) for i in range(len(self.state.Isosurfaces[self.state.contour_by])))
        self.source_manager.modify_contour_props(source_id=self.state.active_view, cur_mesh=self.state.cur_mesh,
                                                 contour_by=self.state.contour_by, Isosurfaces=isosurfaces)
        self.data_holder.write_in(self.state.active_view)
        self.visible_manager.update_view()

    def generate_batch_isosurfaces(self):
        t = deepcopy(self.state.Isosurfaces)
        ran = np.random.uniform(low=self.state.point_data_range[self.state.contour_by][0],
                        high=self.state.point_data_range[self.state.contour_by][1],
                        size=int(self.state.linear_num)).tolist()
        l = []
        for r in ran:
            l.append({"title": str(r), "value": r})
        t[self.state.contour_by] = t[self.state.contour_by] + l
        self.state.Isosurfaces = t
        self.state.batch_dialog = False
        self.state.linear_num = 10