from trame.app import get_server, get_client
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vtk, vuetify3 as vuetify, trame
from trame.widgets.html import *

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor, vtkMapper,
)

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# .vtu file data
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# VTK pipeline variable
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------
server = get_server(client_type="vue3")

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# GUI elements
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("Viewer")

    with layout.toolbar:
        # toolbar components
        vuetify.VSpacer()
        vuetify.VDivider(vertical=True, classes="mx-2")

    with layout.drawer as drawer:
        # drawer components
        drawer.width = 325

    with layout.content:
        with Div(
            style="background-color:pink"
        ):
            Span("酒精过敏")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start(host="127.0.0.1")
        # docker build -t trame-app .
    # docker run --gpus all -it --rm -p 8080:80 trame-app

