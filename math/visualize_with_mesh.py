import open3d as o3d

# STL 파일 경로
stl_file_path = "../models/sample_hull.stl"

# STL 파일을 로드하여 mesh 객체 생성
mesh = o3d.io.read_triangle_mesh(stl_file_path)

# 좌표계 생성
coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10, origin=[0, 0, 0])

# 시각화할 객체 리스트 생성
visualize_objects = [mesh, coordinate_frame]

# 시각화
o3d.visualization.draw_geometries(visualize_objects)
