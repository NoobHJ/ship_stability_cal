import open3d as o3d
import numpy as np
import pandas as pd

def compute_y0_distances(mesh, num_x_points=10):
    x_values = np.linspace(mesh.get_min_bound()[0], mesh.get_max_bound()[0], num=num_x_points)
    y0_distances = []

    for x in x_values:
        query_point = np.array([x, 0, 0], dtype=np.float32)  # Convert query_point to Float32
        scene = o3d.t.geometry.RaycastingScene()
        
        # Convert vertices to Float32
        vertices = np.asarray(mesh.vertices, dtype=np.float32)
        
        # Convert triangles to UInt32
        triangles = np.asarray(mesh.triangles, dtype=np.uint32)

        scene.add_triangles(vertices, triangles)
        closest_point_info = scene.compute_closest_points(np.array([query_point]))
        distance = np.linalg.norm(query_point - closest_point_info['points'][0])
        y0_distances.append(distance)

    return y0_distances

def save_distances_to_csv(y0_distances, csv_file_path):
    df = pd.DataFrame({'x_index': range(1, len(y0_distances) + 1), 'distance': y0_distances})
    df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    # STL 파일 경로
    stl_file_path = "../models/sample_hull.stl"

    # STL 파일을 로드하여 mesh 객체 생성
    mesh = o3d.io.read_triangle_mesh(stl_file_path)

    # y=0 지점에서부터 각 x 위치까지의 거리 계산
    y0_distances = compute_y0_distances(mesh)

    # CSV 파일 경로
    csv_file_path = "../db/y0_distances.csv"

    # 거리를 CSV 파일에 저장
    save_distances_to_csv(y0_distances, csv_file_path)
    print("CSV 파일이 생성되었습니다:", csv_file_path)
