import numpy as np
import pandas as pd

csv_file = "../db/point_cloud.csv"

# CSV 파일 읽기
df = pd.read_csv(csv_file)

# 최대 Z, X 값 구하기
max_z = df['Z'].max()
max_x = df['X'].max()

# 결과를 담을 2D 배열 초기화
result_array = np.zeros((max_z + 1, max_x + 1), dtype=int)

# 각 Z 값에 대해 X, Y 값 찾기
for z in range(max_z + 1):
    # 해당하는 Z 값의 행 가져오기
    z_filtered = df[df['Z'] == z]
    # 해당하는 Z 값이 없으면 0으로 채우기
    if z_filtered.empty:
        continue
    # 해당하는 Z 값이 있는 경우 X, Y 값 가져오기
    for _, row in z_filtered.iterrows():
        result_array[z, row['X']] = row['Y']

# 결과 DataFrame 생성
result_df = pd.DataFrame(result_array)

# CSV 파일로 출력
result_csv_file = "../db/offset.csv"
result_df.to_csv(result_csv_file, index=False)

print("2D CSV 파일이 생성되었습니다:", result_csv_file)
