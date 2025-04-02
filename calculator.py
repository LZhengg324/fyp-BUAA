import numpy as np
from scipy.spatial import ConvexHull


def find_farthest_points_on_plane(bounds, origin, normal):
    """
    找到立方体被平面切割后的截面多边形中距离最远的两个端点。

    参数:
        bounds (list): 立方体范围 [x_min, x_max, y_min, y_max, z_min, z_max]。
        origin (np.ndarray): 平面原点，形状 (3,)。
        normal (np.ndarray): 单位法向量，形状 (3,)。

    返回:
        tuple: 最远的两点，形状均为 (3,)。
        float: 两点之间的距离。
    """
    x_min, x_max, y_min, y_max, z_min, z_max = bounds
    origin = np.array(origin)
    normal = np.array(normal)

    # 定义立方体的 12 条棱
    edges = [
        # 底面 4 条边
        (np.array([x_min, y_min, z_min]), np.array([x_max, y_min, z_min])),
        (np.array([x_min, y_min, z_min]), np.array([x_min, y_max, z_min])),
        (np.array([x_max, y_max, z_min]), np.array([x_max, y_min, z_min])),
        (np.array([x_max, y_max, z_min]), np.array([x_min, y_max, z_min])),
        # 顶面 4 条边
        (np.array([x_min, y_min, z_max]), np.array([x_max, y_min, z_max])),
        (np.array([x_min, y_min, z_max]), np.array([x_min, y_max, z_max])),
        (np.array([x_max, y_max, z_max]), np.array([x_max, y_min, z_max])),
        (np.array([x_max, y_max, z_max]), np.array([x_min, y_max, z_max])),
        # 侧面 4 条边
        (np.array([x_min, y_min, z_min]), np.array([x_min, y_min, z_max])),
        (np.array([x_max, y_min, z_min]), np.array([x_max, y_min, z_max])),
        (np.array([x_min, y_max, z_min]), np.array([x_min, y_max, z_max])),
        (np.array([x_max, y_max, z_min]), np.array([x_max, y_max, z_max])),
    ]

    # 计算每条棱与平面的交点
    intersections = []
    for p1, p2 in edges:
        segment_vec = p2 - p1
        denominator = np.dot(normal, segment_vec)

        # 避免除以零（线段与平面平行）
        if np.abs(denominator) < 1e-10:
            continue

        t = np.dot(normal, origin - p1) / denominator
        if 0 <= t <= 1:
            intersection = p1 + t * segment_vec
            intersections.append(intersection)

    # 去重（浮点数精度问题）
    unique_intersections = []
    for point in intersections:
        if not any(np.allclose(point, u) for u in unique_intersections):
            unique_intersections.append(point)
    unique_intersections = np.array(unique_intersections)

    # 处理点集维度不足的问题
    if len(unique_intersections) < 2:
        raise ValueError("平面未切割立方体或切割后点数不足。")

    try:
        # 尝试添加抖动 (QJ) 计算凸包
        hull = ConvexHull(unique_intersections, qhull_options="QJ")
    except:
        # 降维处理（投影到平面）
        def project_to_2d(points):
            u = np.array([1, 0, 0]) - np.dot(np.array([1, 0, 0]), normal) * normal
            u = u / np.linalg.norm(u)
            v = np.cross(normal, u)
            return np.array([[np.dot(p, u), np.dot(p, v)] for p in points])

        projected_points = project_to_2d(unique_intersections)
        hull = ConvexHull(projected_points)
        hull_points = unique_intersections[hull.vertices]
    else:
        hull_points = unique_intersections[hull.vertices]

    # 找最远点对（后续代码不变）...
    max_distance = 0
    point1, point2 = None, None
    n = len(hull_points)
    for i in range(n):
        for j in range(i + 1, n):
            distance = np.linalg.norm(hull_points[i] - hull_points[j])
            if distance > max_distance:
                max_distance = distance
                point1, point2 = hull_points[i], hull_points[j]

    return (point1, point2), max_distance


# 示例用法
bounds = [0, 0.1, 0, 0.1, 0, 0.01]  # 单位立方体
origin = np.array([0.05, 0.05, 0.005])
normal = np.array([1, 1, 1])
normal = normal / np.linalg.norm(normal)  # 归一化

(p1, p2), max_dist = find_farthest_points_on_plane(bounds, origin, normal)
print("最远的两点:", p1, p2)
print("两点距离:", max_dist)