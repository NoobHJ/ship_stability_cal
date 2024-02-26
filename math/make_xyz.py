import open3d as o3d
import numpy as np
import pandas as pd

def save_point_cloud_to_csv(point_cloud, csv_file_path):
    # CSV 파일에 저장할 좌표 데이터 추출
    points = np.asarray(point_cloud.points)
    
    # y가 음수인 좌표 제거
    points = points[points[:, 1] >= 0]
    
    # 좌표 데이터를 정수로 반올림
    rounded_points = np.round(points).astype(int)
    # Pandas DataFrame으로 변환
    df = pd.DataFrame(data=rounded_points, columns=["X", "Y", "Z"])
    # CSV 파일로 저장
    df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    # STL 파일 경로
    stl_file_path = "../models/sample_hull.stl"
    # stl_file_path = "../models/sample_crapster.stl"

    # STL 파일을 로드하여 mesh 객체 생성
    mesh = o3d.io.read_triangle_mesh(stl_file_path)

    # 좌표계 생성
    coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10, origin=[0, 0, 0])

    # 점을 균일하게 샘플링하여 point cloud 생성
    n_pts = 40000000
    point_cloud = mesh.sample_points_uniformly(n_pts)

    # CSV 파일 경로
    csv_file_path = "../db/point_cloud.csv"

    # point cloud를 CSV 파일에 저장
    save_point_cloud_to_csv(point_cloud, csv_file_path)
    print("CSV 파일이 생성되었습니다:", csv_file_path)
