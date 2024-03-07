# import pandas as pd

# # Simpson's Rule: s는 1(mm or m)로 할 거기 때문에 상관 없음
# def simpsons_rule(y0, y1, y2):
#     return (1 / 3) * (y0 + 4 * y1 + y2)

# # 선형 CSV 파일 읽기
# def read_linear_csv(file_path):
#     return pd.read_csv(file_path)

# # Section Area 계산
# def calculate_section_area(offset_data):
#     section_area = []
#     for i in range(len(offset_data)):
#         area = []
#         for j in range(2, len(offset_data.columns), 2):
#             area.append(simpsons_rule(offset_data.iloc[i, j - 2], 
#                                       offset_data.iloc[i, j - 1], 
#                                       offset_data.iloc[i, j]))
#         section_area.append(area)
#     return section_area

# # Half of Section Area 계산
# def calculate_half_section_area(section_area_data):
#     return pd.DataFrame(section_area_data).sum(axis=1)

# # Section Volume 계산
# def calculate_section_volume(half_section_area_data):
#     section_volume = []
#     for i in range(1, len(half_section_area_data), 2):
#         section_volume.append(simpsons_rule(half_section_area_data[i - 1],
#                                              half_section_area_data[i], 
#                                              half_section_area_data[i + 1]))
#     return section_volume

# def save_to_csv(dataframe, file_path):
#     dataframe.to_csv(file_path)

# if __name__ == "__main__":
#     OFFSET_CSV_PATH = "../db/offset.csv"
#     SECTION_VOLUME_CSV_PATH = "../res/SectionVolume.csv"
#     HALF_SECTION_AREA_CSV_PATH = "../res/HalfSectionArea.csv"

#     offset_data = read_linear_csv(OFFSET_CSV_PATH)
#     section_area_data = calculate_section_area(offset_data)
#     half_section_area_data = calculate_half_section_area(section_area_data)
#     section_volume_data = calculate_section_volume(half_section_area_data)

#     save_to_csv(pd.DataFrame(section_volume_data), SECTION_VOLUME_CSV_PATH)
#     save_to_csv(pd.DataFrame(half_section_area_data), HALF_SECTION_AREA_CSV_PATH)

#     total_volume = sum(section_volume_data) * 2
#     print("Total section volume = ", total_volume, "mm^3")
