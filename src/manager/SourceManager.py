from copy import deepcopy
from typing import Dict, List, Tuple

from paraview import simple

class SourceManager:
    def __init__(self):
        self.sources = dict()
        self.id_counter = 1

    def add_source(self, source) -> int:
        source_id = self.id_counter
        self.sources[source_id] = source
        self.id_counter += 1
        return source_id

    # def add_source_real(self, source: Dict) -> int:
    #     source_id = self.id_counter
    #     self.sources[source_id] = source
    #     self.id_counter += 1
    #     return source_id

    def get_source(self, source_id: int):
        return self.sources[source_id]

    # def get_source_real(self, source_id: int, time_step: int):
    #     return self.sources[source_id][time_step]

    def get_new_id(self) -> int:
        return self.id_counter

    # -----------------------------------------------------------------------------
    # File Process
    # -----------------------------------------------------------------------------

    def get_point_data_field_and_range(self, source_id: int) -> Tuple[List[str], Dict[str, Tuple[float, float]]]:
        point_data = self.sources[source_id].PointData
        point_data_field = list(point_data.keys())
        point_data_range = {}
        for pd in point_data:
            point_data_range[pd.Name] = pd.GetRange()
        return point_data_field, point_data_range

    # def get_point_data_field_and_range_real(self, source_id: int) -> Tuple[List[str], Dict[str, Tuple[float, float]]]:
    #     point_data = list(self.sources[source_id].values())[0].PointData
    #     point_data_field = list(point_data.keys())
    #     point_data_range = {}
    #     for pd in point_data:
    #         point_data_range[pd.Name] = pd.GetRange()
    #     return point_data_field, point_data_range

    def get_scalar_vector_field_and_range(self, source_id: int) -> Tuple[List[str], List[str]]:

        point_data = self.sources[source_id].PointData

        scalar_field = list()
        vector_field = list()

        for pd in point_data:
            if pd.GetNumberOfComponents() == 1:
                scalar_field.append(pd.Name)
            else:
                vector_field.append(pd.Name)

        return scalar_field, vector_field

    # def get_scalar_vector_field_and_range_real(self, source_id: int) -> Tuple[List[str], List[str]]:
    #
    #     point_data = list(self.sources[source_id].values())[0].PointData
    #
    #     scalar_field = list()
    #     vector_field = list()
    #
    #     for pd in point_data:
    #         if pd.GetNumberOfComponents() == 1:
    #             scalar_field.append(pd.Name)
    #         else:
    #             vector_field.append(pd.Name)
    #
    #     return scalar_field, vector_field

    def delete_module(self, source_id: int):
        self.sources.pop(source_id)

    def reboot_all_for_new_main_module(self):
        self.sources.clear()
        print("source_manager", self.sources)

    # -----------------------------------------------------------------------------
    # Slice
    # -----------------------------------------------------------------------------

    def add_slice(self, source_id: int):
        source = self.sources[source_id]
        new_source = simple.Slice(Input=source)
        new_source.SliceType = "Plane"
        return self.add_source(new_source)

    # def add_slice_real(self, source_id: int):
    #     source_set = self.sources[source_id]
    #     new_source = {}
    #     for time_step, source in source_set.items():
    #         new_source[time_step] = simple.Slice(Input=source)
    #         new_source[time_step].SliceType = "Plane"
    #     return self.add_source(new_source)

    def modify_slice_props(self, source_id: int, origin: List[float], normal: List[float]):
        # print("origin", origin)
        # print("normal", type(normal), type(normal[0]))
        slice_filter = self.sources[source_id]
        slice_filter.SliceType.Origin = origin
        slice_filter.SliceType.Normal = normal

    # def modify_slice_props_real(self, source_id: int, origin: List[float], normal: List[float]):
    #     # print("origin", origin)
    #     # print("normal", type(normal), type(normal[0]))
    #     source = self.sources[source_id]
    #     for slice_filter in source.values():
    #         slice_filter.SliceType.Origin = origin
    #         slice_filter.SliceType.Normal = normal

    # -----------------------------------------------------------------------------
    # Contour
    # -----------------------------------------------------------------------------

    def add_contour(self, source_id: int):
        source = self.sources[source_id]
        new_source = simple.Contour(Input=source)
        return self.add_source(new_source)

    # def add_contour_real(self, source_id: int):
    #     source_set = self.sources[source_id]
    #     new_source = {}
    #     for time_step, source in source_set.items():
    #         new_source[time_step] = simple.Contour(Input=source)
    #     return self.add_source(new_source)

    def modify_contour_props(self, source_id: int, cur_mesh: str, contour_by: str, Isosurfaces: List[float]):
        contour_filter = self.sources[source_id]
        contour_filter.ContourBy = [cur_mesh, contour_by]
        contour_filter.Isosurfaces = Isosurfaces

    # def modify_contour_props_real(self, source_id: int, cur_mesh: str, contour_by: str, Isosurfaces: List[float]):
    #     source = self.sources[source_id]
    #     for contour_filter in source.values():
    #         contour_filter.ContourBy = [cur_mesh, contour_by]
    #         contour_filter.Isosurfaces = Isosurfaces

    # -----------------------------------------------------------------------------
    # Glyph
    # -----------------------------------------------------------------------------

    def add_glyph(self, source_id: int):
        source = self.sources[source_id]
        new_source = simple.Glyph(Input=source)
        return self.add_source(new_source)

    # def add_glyph_real(self, source_id: int):
    #     source_set = self.sources[source_id]
    #     new_source = {}
    #     for time_step, source in source_set.items():
    #         new_source[time_step] = simple.Glyph(Input=source)
    #     return self.add_source(new_source)

    def modify_glyph_props(self, source_id: int, glyph_type: str,
                           orientation_array: str, scale_array: str,
                           vector_scale_mode: str, scale_factor: float):
        glyph_filter = self.sources[source_id]
        glyph_filter.GlyphType = glyph_type
        glyph_filter.OrientationArray = orientation_array
        glyph_filter.ScaleArray = scale_array
        glyph_filter.VectorScaleMode = vector_scale_mode
        glyph_filter.ScaleFactor = scale_factor

    # def modify_glyph_props(self, source_id: int, glyph_type: str,
    #                        orientation_array: str, scale_array: str,
    #                        vector_scale_mode: str, scale_factor: float):
    #     source = self.sources[source_id]
    #     for glyph_filter in source.values():
    #         # print("glyph_filter.VectorScaleMode", glyph_filter.VectorScaleMode)
    #         glyph_filter.GlyphType = glyph_type
    #         glyph_filter.OrientationArray = orientation_array
    #         glyph_filter.ScaleArray = scale_array
    #         glyph_filter.VectorScaleMode = vector_scale_mode
    #         glyph_filter.ScaleFactor = scale_factor

    # -----------------------------------------------------------------------------
    # Stream Tracer
    # -----------------------------------------------------------------------------

    def add_stream_tracer(self, source_id: int):
        source = self.sources[source_id]
        new_source = simple.StreamTracer(Input=source)
        return self.add_source(new_source)

    # def add_stream_tracer_real(self, source_id: int):
    #     source_set = self.sources[source_id]
    #     new_source = {}
    #     for time_step, source in source_set.items():
    #         new_source[time_step] = simple.StreamTracer(Input=source)
    #     return self.add_source(new_source)

    def modify_stream_tracer_props(self, source_id: int, vector: str, integration_direction: str,
                                   integrator_type: str, msl_value: float, resolution: int,
                                   point1_x: float, point1_y: float, point1_z: float,
                                   point2_x: float, point2_y: float, point2_z: float):
        st_filter = self.sources[source_id]
        st_filter.Vectors = ["POINTS", vector]
        st_filter.IntegrationDirection = integration_direction
        st_filter.IntegratorType = integrator_type
        st_filter.MaximumStreamlineLength = msl_value
        st_filter.SeedType = "Line"
        st_filter.SeedType.Resolution = resolution
        st_filter.SeedType.Point1 = [point1_x, point1_y, point1_z]
        st_filter.SeedType.Point2 = [point2_x, point2_y, point2_z]

    # def modify_stream_tracer_props_real(self, source_id: int, vector: str, integration_direction: str,
    #                                integrator_type: str, msl_value: float, resolution: int,
    #                                point1_x: float, point1_y: float, point1_z: float,
    #                                point2_x: float, point2_y: float, point2_z: float):
    #     source = self.sources[source_id]
    #     for st_filter in source.values():
    #         print(vector, integration_direction, integrator_type, msl_value, resolution)
    #         st_filter.Vectors = ["POINTS", vector]
    #         st_filter.IntegrationDirection = integration_direction
    #         st_filter.IntegratorType = integrator_type
    #         st_filter.MaximumStreamlineLength = msl_value
    #         st_filter.SeedType = "Line"
    #         st_filter.SeedType.Resolution = resolution
    #         st_filter.SeedType.Point1 = [point1_x, point1_y, point1_z]
    #         st_filter.SeedType.Point2 = [point2_x, point2_y, point2_z]

    # -----------------------------------------------------------------------------
    # Threshold
    # -----------------------------------------------------------------------------

    def add_threshold(self, source_id: int):
        source = self.sources[source_id]
        new_source = simple.Threshold(Input=source)
        return self.add_source(new_source)

    # def add_threshold_real(self, source_id: int):
    #     source_set = self.sources[source_id]
    #     new_source = {}
    #     for time_step, source in source_set.items():
    #         new_source[time_step] = simple.Threshold(Input=source)
    #     return self.add_source(new_source)

    def modify_threshold_props(self, source_id: int, scalar: str,
                               lower_value: float, upper_value: float, method: str,
                               all_scalars: bool, use_continuous_cell_range: bool, invert: bool):
        threshold_filter = self.sources[source_id]
        threshold_filter.Scalars = scalar
        threshold_filter.LowerThreshold = lower_value
        threshold_filter.UpperThreshold = upper_value
        threshold_filter.ThresholdMethod = method
        threshold_filter.AllScalars = all_scalars
        threshold_filter.UseContinuousCellRange = use_continuous_cell_range
        threshold_filter.Invert = invert

    # def modify_threshold_props_real(self, source_id: int, scalar: str,
    #                            lower_value: float, upper_value: float, method: str,
    #                            all_scalars: bool, use_continuous_cell_range: bool, invert: bool):
    #     source = self.sources[source_id]
    #     for threshold_filter in source.values():
    #         threshold_filter.Scalars = scalar
    #         threshold_filter.LowerThreshold = lower_value
    #         threshold_filter.UpperThreshold = upper_value
    #         threshold_filter.ThresholdMethod = method
    #         threshold_filter.AllScalars = all_scalars
    #         threshold_filter.UseContinuousCellRange = use_continuous_cell_range
    #         threshold_filter.Invert = invert