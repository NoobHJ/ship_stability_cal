import open3d as o3d
import numpy as np
import pandas as pd
# import sys

async def save_point_cloud_to_csv(point_cloud, csv_file_path):
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

async def make_xyz(stl_file_path, csv_file_path):
    try :
        # STL 파일을 로드하여 mesh 객체 생성
        mesh = o3d.io.read_triangle_mesh(stl_file_path)

        # 점을 균일하게 샘플링하여 point cloud 생성
        n_pts = 10000000
        point_cloud = mesh.sample_points_uniformly(n_pts)

        # point cloud를 CSV 파일에 저장
        await save_point_cloud_to_csv(point_cloud, csv_file_path)
        print("CSV 파일이 생성되었습니다:", csv_file_path)

    except Exception as e:
        print(e)

# # stl_file_path = "../uploaded_stl_files/" + sys.argv[1]
# stl_file_path = "../uploaded_stl_files/test1.stl"
# # stl_file_path = "../models/sample_hull.stl"

# # CSV 파일 경로
# csv_file_path = "../db/test1.csv"

#     # make_xyz 함수 호출
# make_xyz(stl_file_path, csv_file_path)
