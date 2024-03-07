import pandas as pd

# Simpson's Rule s는 1(mm or m)로 할거기 때문에 상관 없음
def simpson(y0, y1, y2):
    return (1/3) * (y0 + 4 * y1 + y2)

# index갯수가 3의배수라면 아래 식 사용해야 할듯
def simpson2(y0, y1, y2, y3):
    return (3/8) * (y0 + 3 * y1 + 3 * y2 + y3)

# 선형 CSV 파일 읽기
offset = pd.read_csv("../db/offset.csv")

# Section Area 계산
section_area = []
for i in range(len(offset)):  # offset의 행의 수에 해당하는 값으로 수정
    a = []
    for j in range(2, len(offset.columns), 2):  # offset의 열의 수에 해당하는 값으로 수정
        a.append(simpson(offset.iloc[i, j-2], 
                         offset.iloc[i, j-1], 
                         offset.iloc[i, j]))
    section_area.append(a)

# Half of Section Area 계산
half_of_section_area = pd.DataFrame(section_area).sum(axis=1)

# Section Volume 계산
section_volume = []
for i in range(2, len(half_of_section_area), 2):
    section_volume.append(simpson(half_of_section_area[i-2], 
                                  half_of_section_area[i-1], 
                                  half_of_section_area[i]))

# # Section Volume을 CSV 파일로 저장
# section_volume_df = pd.DataFrame(section_volume)
# section_volume_df.to_csv("../res/SectionVolume.csv")

# # 반으로 나눈 Section Area를 CSV 파일로 저장
# half_of_section_area_df = pd.DataFrame(half_of_section_area)
# half_of_section_area_df.to_csv("../res/HalfSectionArea.csv")

# print("Halfvolmld=",sum(section_volume))
print("section_volume = ", sum(section_volume)*2, "mm^3")


# water Area 계산
waterplane_area = []
for i in range(2, len(offset.index), 2):  # offset의 행의 수에 해당하는 값으로 수정
    a = []
    for j in range(len(offset.columns)):  # offset의 열의 수에 해당하는 값으로 수정
        a.append(simpson(offset.iloc[i-2, j], 
                         offset.iloc[i-1, j], 
                         offset.iloc[i, j]))
    waterplane_area.append(a)


waterplane_area_df = pd.DataFrame(waterplane_area).sum(axis=1)

waterplane_volume = []
# for i in range(1, len(waterplane_area_df)-2, 2):  # 마지막 인덱스에 접근하지 않도록 수정
#     waterplane_volume.append(simpson(waterplane_area_df[i-1], waterplane_area_df[i], waterplane_area_df[i+1]))

for i in range(3, len(waterplane_area_df), 3):  
    waterplane_volume.append(simpson2(waterplane_area_df[i-3], 
                                     waterplane_area_df[i-2], 
                                     waterplane_area_df[i-1],
                                     waterplane_area_df[i]))

# waterplane_volume을 CSV 파일로 저장
waterplane_volume_df = pd.DataFrame(waterplane_volume)
waterplane_volume_df.to_csv("../res/WaterplaneVolume.csv")

print(waterplane_area_df)
print("section_volume = ", sum(waterplane_volume)*2, "mm^3")
