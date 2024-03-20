import numpy as np
import pandas as pd

def simpson(y0, y1, y2):
    return (1/3) * (y0 + 4 * y1 + y2)

def moment_simpson(y0,y1,y2,s1,s2,s3):
    return (1/3) * (y0 * s1 + 4 * y1 * s2 + y2 * s3)

def second_moment_simpson(y0,y1,y2,s1,s2,s3):
    return (1/3)**3 * (y0 * s1 ** 2 + 4 * y1 * s2 ** 2 + y2 * s3 ** 2)

def simpson_5_8_1(y0,y1,y2):
    return (1/12) * (5 * y0 + 8 * y1 - y2)

def calculate_waterplane_area(data, result_list):
    for i in range(len(data.index)):
        a = []
        for j in range(2, len(data.columns), 1):
            a.append(simpson_5_8_1(data.iloc[i,j-2], 
                            data.iloc[i,j-1], 
                            data.iloc[i,j]))
        result_list.append(a)

def calculate_volume(data, result_list):    
        for i in range(2, len(data), 1):
            result_list.append(simpson_5_8_1(data[i-2],
                                data[i-1],
                                data[i]))
    

def calculate_section_area(data, result_list):
    for j in range(len(data.columns)):
        a = []
        for i in range(2, len(data.index), 2):
            a.append(simpson(data.iloc[i-2, j], 
                            data.iloc[i-1, j], 
                            data.iloc[i, j]))
        result_list.append(a)

def cal_design(waterplane_weight, total_weight):
    stop_index = 0
    middle_weight = 0

    for i, weight in enumerate(waterplane_weight):
        middle_weight += weight
        if middle_weight >= (total_weight/2):
            stop_index = i
            break
    design_draft = stop_index + 1
    return design_draft

def calculate_mass_center_x(data):
    first_moment_y = []
    for i in range(len(data.index)):
        a = []
        for j in range(2, len(data.columns), 2):
            a.append(data.iloc[i,j] * (j-1))
        first_moment_y.append(sum(a))

    total_moment = sum(first_moment_y)
    total_y = sum(data.iloc[:, 1::2].sum())

    masscenter_x = total_moment / total_y
    return masscenter_x

def calculate_mass_center_z(data, waterplane_volume):
    first_moment_z = []
    for i in range(len(data.index)):
        a = []
        for j in range(2, len(data.columns), 2):
            a.append(simpson(data.iloc[i,j-2], 
                            data.iloc[i,j-1], 
                            data.iloc[i,j]))
        first_moment_z.append(sum(a))

    total_momentz = []

    for i in range(2, len(first_moment_z), 2):
        s1 = 0.5 + i - 2
        s2 = 0.5 + i - 1
        s3 = 0.5 + i
        total_momentz.append(moment_simpson(first_moment_z[i-2], 
                                            first_moment_z[i-1], 
                                            first_moment_z[i], 
                                            s1, s2, s3))

    masscenter_z = sum(total_momentz) / (sum(waterplane_volume))
    return masscenter_z

def calculate_moment_of_inertia(data, result_list, masscenter_x):
    for j in range(len(data.columns)):
        a = []
        for i in range(2, len(data.index), 2):
            s1 = -masscenter_x + 0.5 + i - 2
            s2 = -masscenter_x + 0.5 + i - 1
            s3 = -masscenter_x + 0.5 + i
            a.append(second_moment_simpson(data.iloc[i-2, j], 
                                           data.iloc[i-1, j], 
                                           data.iloc[i, j],
                                           s1, s2, s3))
        result_list.append(sum(a))

def cal_run():
    csv_file = "./offset.csv"
    # 선형 CSV 파일 읽기
    offset = pd.read_csv(csv_file)

    # 변수 선언
    density = 1.025 # g/mm^3
    light_weight = 3000000 # 경하중량
    dead_weight = 3000000 # 화물중량
    total_weight = light_weight + dead_weight #최종중량

    # waterplane_area 계산
    waterplane_area = []
    calculate_waterplane_area(offset, waterplane_area)
    half_of_waterplane_area = pd.DataFrame(waterplane_area).sum(axis=1)

    waterplane_volume = []
    calculate_volume(half_of_waterplane_area,waterplane_volume)
    print("volume from waterplane = ", sum(waterplane_volume)*2, "mm^3")

    #section_area계산
    section_area = []
    calculate_section_area(offset, section_area)
    half_of_section_area = pd.DataFrame(section_area).sum(axis=1)

    section_volume = []
    calculate_volume(half_of_section_area,section_volume)
    print("volume from section_volume = ", sum(section_volume)*2, "mm^3")

    # 배수량 구하기
    section_weight = [x * density for x in section_volume]
    waterplane_weight = [x * density for x in waterplane_volume]
    print("weight from section = ", sum(section_weight)*2, "g")
    print("weight from waterplane = ", sum(waterplane_weight)*2, "g")

    # 흘수선 정하기
    total_weight = light_weight + dead_weight  # 최종중량 설정
    design_draft = cal_design(waterplane_weight, total_weight)

    print("design volume =", total_weight / 1.025, "mm^3")
    print("design draft =", design_draft, "mm")
    
    # First Moment
    #mass center length
    masscenter_x = calculate_mass_center_x(offset)
    LCB = masscenter_x

    print("mass center x =", masscenter_x)
    print("mass center y =", 0)

    # mass center height
    masscenter_z = calculate_mass_center_z(offset, waterplane_volume)
    print("masscenter_z =", masscenter_z)


    # second moment I
    moment_of_inertia_tranceverse = []
    calculate_moment_of_inertia(offset, moment_of_inertia_tranceverse, masscenter_x)
    print(len(moment_of_inertia_tranceverse))
    print(sum(moment_of_inertia_tranceverse))

cal_run()
