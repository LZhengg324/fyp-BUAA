from typing import List, Dict

import paraview.web.venv  # Available in PV 5.10

from trame.widgets import vuetify3 as vuetify, trame
from trame_server import Server
from trame.app import get_server
from paraview import simple
from Source.VisibleManager import VisibleManager
# def TimeStep():
#     with vuetify.VRow(
#             align="center",
#             justify="center",
#     ):
#         vuetify.VBtn(
#             icon="mdi-minus",
#             click="trigger('minus_cur_step')",
#             # disabled=(("cur_step",) == min(writeIntervals)),
#             # v_bind={"disabled": "cur_step === Math.min(...writeIntervals)"},
#             classes="ma-2",
#         )
#         vuetify.VLabel(
#             text=("cur_step",),
#             classes="ma-3",
#             hide_details=True,
#         )
#         vuetify.VBtn(
#             icon="mdi-plus",
#             click="trigger('add_cur_step')",
#             # disabled=("state.cur_step" == max(writeIntervals),),
#             classes="ma-2",
#         )
#
# ctrl, state = server.controller, server.state
#
# @ctrl.trigger("add_cur_step")
# def add_cur_time_trigger():
#     if state.cur_step == max(writeIntervals):
#         return
#     state.cur_step += step
#
# @ctrl.trigger("minus_cur_step")
# def minus_cur_time_trigger():
#     if state.cur_step == min(writeIntervals):
#         return
#     state.cur_step -= step

class TimeStep:
    def __init__(self, server: Server, visible_manager: VisibleManager):
        self.server = server
        self.ctrl = server.controller
        self.state = server.state
        self.visible_manager = visible_manager

        @self.ctrl.trigger("add_cur_step")
        def add_cur_time_trigger():
            if self.state.cur_step_ptr >= len(self.state.write_interval) - 1:
                return
            self.state.cur_step_ptr += 1
            self.state.cur_step = self.state.write_interval[self.state.cur_step_ptr]


        @self.ctrl.trigger("minus_cur_step")
        def minus_cur_time_trigger():
            if self.state.cur_step_ptr <= 0:
                return
            self.state.cur_step_ptr -= 1
            self.state.cur_step = self.state.write_interval[self.state.cur_step_ptr]

        @self.state.change("cur_step")
        def update_view(cur_step, **kwargs):
            if self.state.write_interval[self.state.cur_step_ptr] != self.state.cur_step:
                self.state.cur_step_ptr = self.state.write_interval.index(self.state.cur_step)
            print("cur_step", cur_step, "ptr", self.state.cur_step_ptr)
            visible_manager.update_view()

    # -----------------------------------------------------------------------------
    # GUI Components
    # -----------------------------------------------------------------------------

    def time_step(self):
        with vuetify.VRow(
                align="center",
                justify="center",
        ):
            vuetify.VLabel(
                "Time: ",
                hide_details=True,
                classes="mx-2"
            )
            vuetify.VSelect(
                v_model=("cur_step", ),
                items=("write_interval",),
                hide_details=True,
                dense=True,
                variant="outlined",
                style="max-width: 100px;",
            )
            vuetify.VBtn(
                icon="mdi-minus",
                click="trigger('minus_cur_step')",
                classes="ma-2",
            )
            vuetify.VLabel(
                "{{cur_step_ptr + 1}}",
                classes="ma-3",
                hide_details=True,
            )
            vuetify.VBtn(
                icon="mdi-plus",
                click="trigger('add_cur_step')",
                # disabled=("state.cur_step" == max(writeIntervals),),
                classes="ma-2",
            )
