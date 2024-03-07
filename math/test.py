import pandas as pd

# offset 테이블을 읽어옵니다.
offset = pd.read_csv("../db/offset.csv")
masscenter_x = 472.2886051286032

def calculate_moment_of_inertia(data, result_list, masscenter_x):
    for j in range(len(data.columns)):
        Ixx = 0
        Iyy = 0
        for i in range(2, len(data.index), 2):
            s1 = 0.5 + i - 2
            s2 = 0.5 + i - 1
            s3 = 0.5 + i
            
            # Ixx 계산
            Ixx += (1/3)**2 *(data.iloc[i-2, j] * (s1 ** 2) +
                    4 * data.iloc[i-1, j] * (s2 ** 2) +
                    data.iloc[i, j] * (s3 ** 2))
            
            # Iyy 계산
            Iyy += (1/3)**2 * (data.iloc[i-2, j] * (masscenter_x ** 2) +
                    4 * data.iloc[i-1, j] * (masscenter_x ** 2) +
                    data.iloc[i, j] * (masscenter_x ** 2))
        
        result_list.append(Ixx)
        result_list.append(Iyy)

# Ixx와 Iyy 계산
moment_of_inertia = []
calculate_moment_of_inertia(offset, moment_of_inertia, masscenter_x)

Ixx = sum(moment_of_inertia[::2])
Iyy = sum(moment_of_inertia[1::2])

print("Ixx (길이방향 Moment of Inertia):", Ixx)
print("Iyy (횡방향 Moment of Inertia):", Iyy)
