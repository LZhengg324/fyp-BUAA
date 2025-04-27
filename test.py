import paraview.web.venv  # Available in PV 5.10

from pathlib import Path
from trame.app import get_server
from trame.widgets import vuetify3 as vuetify, paraview
from trame.ui.vuetify3 import SinglePageLayout

from paraview import simple
import time
from trame_vuetify.ui.vuetify3 import SinglePageWithDrawerLayout

# -----------------------------------------------------------------------------
# trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type = "vue3")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

# 1. 获取渲染窗口
render_view = simple.GetActiveViewOrCreate('RenderView')
print(render_view.ListProperties())
# render_view.InteractionMode = "2D"

# 2. 读取 VTK 数据
vtk_file = Path(__file__).parent.joinpath("File").joinpath("host2").joinpath("VTK").joinpath("host_40.vtk")
print(vtk_file)
file_reader = simple.LegacyVTKReader(FileNames=[str(vtk_file)])
# print(simple.XMLMultiBlockDataReader())
# file_reader = simple.LegacyVTKReader(FileNames=vtk_file)
print(file_reader.PointData)
# print(file_reader.FileNameInfo())
file_reader.UpdatePipeline()
print(file_reader.GetDataInformation().GetBounds())
print(list(file_reader.CellData.keys()))
scalar_field = 'p'

######################################
#---------------Slice----------------#
######################################
# 3. 创建切片过滤器
# slice_filter = simple.Slice(Input=file_reader)
# slice_filter.SliceType.Origin = [0.05, 0.05, 0.005]  # 切片平面原点
# slice_filter.SliceType.Normal = [0, 1, 0]
# slice_filter2 = simple.Slice(Input=file_reader)
# glyph = simple.Glyph(Input=slice_filter)
# print(glyph.ListProperties())
# glyph.GlyphType = "Arrow"
# glyph.OrientationArray = "U"
# glyph.ScaleArray = "U"  # 让缩放依据矢量数据
# glyph.VectorScaleMode = "Scale by Magnitude"  # 让矢量长度按其大小缩放
# glyph.ScaleFactor = 0.01
# seeds = simple.Line()  # 选择种子点
# seeds.Point1 = [0, 0, 0.005]
# seeds.Point2 = [0.1, 0.1, 0.005]

# stream_tracer = simple.StreamTracer(Input=slice_filter)
# print(dir(slice_filter))
# print(slice_filter.PointData['p'].GetRange())
# print(stream_tracer.ListProperties())
# print(stream_tracer.IntegratorType)
# stream_tracer.Vectors = ['POINTS', 'U']
# stream_tracer.MaximumStreamlineLength = 0.1
# stream_tracer.SeedType = "Line"
#
# print(stream_tracer.SeedType.ListProperties())
# print(stream_tracer.SeedType.Point1)
# print(stream_tracer.SeedType.Point2)
# stream_tracer.SeedType.Point1 = [0, 0, 0.005]  # 线起点
# stream_tracer.SeedType.Point2 = [0.1, 0.1, 0.005]   # 线终点
# stream_tracer.SeedType.Resolution = 10
data_bounds = file_reader.GetDataInformation().GetBounds()

#---------------------Test------------------------#
# 3. 获取标量字段 "p" 的值范围
if "p" in file_reader.PointData.keys():
    value_range = file_reader.PointData["p"].GetRange()
    print(f"Value range of 'p': {value_range}")

    # 设置 Isosurfaces 的值为范围的中点
    contour_value = (value_range[0] + value_range[1]) / 2
    state.contour_value = contour_value  # 用于动态调整
# print(f"Data bounds: {data_bounds}")  # 输出数据范围
# print(f"Slice origin: {slice_filter.SliceType.Origin}")  # 输出切片位置

# slice_filter.SliceType = "Plane"
# slice_filter2.SliceType = "Plane"
#
# # 设置切片参数
#       # 切片法线方向（X轴方向）
# slice_filter2.SliceType.Origin = [0.0, 0.09, 0]  # 切片平面原点
# slice_filter2.SliceType.Normal = [0, 0.5, 0]        # 切片法线方向（X轴方向）

######################################
#---------------Slice----------------#
######################################

######################################
#--------------Contour---------------#
######################################
# contour_filter = simple.Contour(Input=slice_filter)
# print(contour_filter.ListProperties())
# contour_filter.ContourBy = scalar_field  # 替换为数据的标量字段
# contour_filter.Isosurfaces = [state.contour_value]
# contour_filter.ColorBy = ["Points", "p"]
######################################
#--------------Contour---------------#
######################################

# 4. 显示切片结果
# slice_display = simple.Show(slice_filter, render_view)
# glyph_display = simple.Show(glyph, render_view)
# st_display = simple.Show(stream_tracer, render_view)
# slice2_display = simple.Show(slice_filter2, render_view)
# contour_display = simple.Show(contour_filter, render_view)
display = simple.Show(file_reader, render_view)

# print(list(slice_filter.PointData.keys()))
# # 4. 选择标量字段 scalar_field 进行颜色映射
# #     simple.ColorBy(contour_display, ('POINTS', scalar_field))
# simple.ColorBy(glyph_display, ('POINTS', 'U'))
# simple.ColorBy(st_display, ('POINTS', 'U'))
simple.ColorBy(display, ('POINTS', 'p'))
#     simple.ColorBy(contour_display, ('POINTS', scalar_field))






# 5. 更新颜色条
# glyph_display.SetScalarBarVisibility(render_view, True)
# contour_display.SetScalarBarVisibility(render_view, True)
simple.UpdateScalarBars(render_view)
# 设置背景颜色
render_view.Background = [1, 1, 1]
render_view.ResetCamera()

# 6. 强制渲染更新
simple.Render(render_view)

# 7. 创建 trame 界面
with SinglePageWithDrawerLayout(server) as layout:
    with layout.content:
        # html_view = paraview.VtkLocalView(render_view, interactive_ratio=1)
        html_view = paraview.VtkRemoteView(render_view, interactive_ratio=1)
        ctrl.view_update = html_view.update
        ctrl.view_reset_camera = html_view.reset_camera

    # 手动添加 Legend
    with layout.toolbar:
        vuetify.VBtn("Reset Camera", click=ctrl.view_reset_camera)
        vuetify.VBtn("update", click=ctrl.view_update)
        vuetify.VSpacer()


# 8. 启动服务器
if __name__ == '__main__':
    ctrl.view_update()  # 确保 UI 更新
    server.start(host="127.0.0.1")
