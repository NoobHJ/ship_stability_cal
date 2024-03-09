import numpy as np
import pandas as pd


# Simpson's Rule s는 1(mm or m)로 할거기 때문에 상관 없음
async def simpson(y0, y1, y2):
    return (1 / 3) * (y0 + 4 * y1 + y2)


# index갯수가 홀수라면 2배수만큼 1번룰 사용, 마지막 index들에만 아래식 사용하자
async def simpson2(y0, y1, y2, y3):
    return (3 / 8) * (y0 + 3 * y1 + 3 * y2 + y3)


async def moment_simpson(y0, y1, y2, s1, s2, s3):
    return (1 / 3) * (y0 * s1 + 4 * y1 * s2 + y2 * s3)


async def second_moment_simpson(y0, y1, y2, s1, s2, s3):
    return (1 / 3) ** 3 * (y0 * s1**2 + 4 * y1 * s2**2 + y2 * s3**2)


async def calculate_waterplane_area(data, result_list):
    for i in range(len(data.index)):
        a = []
        for j in range(2, len(data.columns), 2):
            a.append(
                await simpson(data.iloc[i, j - 2], data.iloc[i, j - 1], data.iloc[i, j])
            )
        result_list.append(a)
    return result_list


async def calculate_volume(data, result_list):
    if len(data) % 2 == 0:
        for i in range(2, len(data), 2):
            result_list.append(
                await simpson(
                    data[i - 2],
                    data[i - 1],
                    data[i],
                )
            )
    else:
        for i in range(2, len(data) - 2, 2):
            result_list.append(
                await simpson(
                    data.iloc[i - 2],
                    data.iloc[i - 1],
                    data.iloc[i],
                )
            )
        result_list.append(
            await simpson2(data.iloc[-4], data.iloc[-3], data.iloc[-2], data.iloc[-1])
        )
    return result_list


async def calculate_section_area(data, result_list):
    for j in range(len(data.columns)):
        a = []
        for i in range(2, len(data.index), 2):
            a.append(
                await simpson(data.iloc[i - 2, j], data.iloc[i - 1, j], data.iloc[i, j])
            )
        result_list.append(a)
    return result_list


async def calculate_moment_of_inertia(data, result_list, masscenter_x):
    for j in range(len(data.columns)):
        a = []
        for i in range(2, len(data.index), 2):
            s1 = -masscenter_x + 0.5 + i - 2
            s2 = -masscenter_x + 0.5 + i - 1
            s3 = -masscenter_x + 0.5 + i
            a.append(
                await second_moment_simpson(
                    data.iloc[i - 2, j],
                    data.iloc[i - 1, j],
                    data.iloc[i, j],
                    s1,
                    s2,
                    s3,
                )
            )
        result_list.append(sum(a))
    return result_list


async def cal_run(offset_path):
    csv_file = offset_path
    # 선형 CSV 파일 읽기
    offset = pd.read_csv(csv_file)

    # 변수 선언
    density = 1.025  # g/mm^3
    light_weight = 3000000  # 경하중량
    dead_weight = 3000000  # 화물중량
    total_weight = light_weight + dead_weight  # 최종중량

    # waterplane_area 계산
    waterplane_area = []
    waterplane_area = await calculate_waterplane_area(offset, waterplane_area)
    half_of_waterplane_area = pd.DataFrame(waterplane_area).sum(axis=1)

    waterplane_volume = []
    waterplane_volume = await calculate_volume(
        half_of_waterplane_area, waterplane_volume
    )
    print("volume from waterplane = ", sum(waterplane_volume) * 2, "mm^3")

    # section_area계산
    section_area = []
    section_area = await calculate_section_area(offset, section_area)
    half_of_section_area = pd.DataFrame(section_area).sum(axis=1)

    section_volume = []
    section_volume = await calculate_volume(half_of_section_area, section_volume)
    print("volume from section_volume = ", sum(section_volume) * 2, "mm^3")

    # 배수량 구하기
    section_weight = [x * density for x in section_volume]
    waterplane_weight = [x * density for x in waterplane_volume]
    print("weight from section = ", sum(section_weight) * 2, "g")
    print("weight from waterplane = ", sum(waterplane_weight) * 2, "g")

    # 흘수선 정하기
    stop_index = 0
    middle_weight = 0
    for i, weight in enumerate(waterplane_weight):
        middle_weight += weight
        if middle_weight >= (total_weight / 2):
            stop_index = i
            break
    design_draft = stop_index * 2 + 2

    print("design volume =", total_weight / 1.025, "mm^3")
    print("design draft =", design_draft, "mm")

    # First Moment
    # mass center length
    first_moment_y = []
    for i in range(len(offset.index)):
        a = []
        for j in range(2, len(offset.columns), 2):
            a.append(offset.iloc[i, j] * (j - 1))
        first_moment_y.append(sum(a))

    total_moment = sum(first_moment_y)
    total_y = sum(offset.iloc[:, 1::2].sum())

    masscenter_x = total_moment / total_y
    LCB = masscenter_x

    print("mass center x =", masscenter_x)
    # print("LCB =", LCB)
    print("mass center y =", 0)

    # mass center height
    first_moment_z = []

    for i in range(len(offset.index)):
        a = []
        for j in range(2, len(offset.columns), 2):
            a.append(
                await simpson(
                    offset.iloc[i, j - 2], offset.iloc[i, j - 1], offset.iloc[i, j]
                )
            )
        first_moment_z.append(sum(a))

    total_momentz = []
    for i in range(2, len(first_moment_z), 2):
        s1 = 0.5 + i - 2
        s2 = 0.5 + i - 1
        s3 = 0.5 + i
        total_momentz.append(
            await moment_simpson(
                first_moment_z[i - 2],
                first_moment_z[i - 1],
                first_moment_z[i],
                s1,
                s2,
                s3,
            )
        )

    masscenter_z = sum(total_momentz) / (sum(waterplane_volume))
    print("mass center z =", masscenter_z)

    # total_momentx_df = pd.DataFrame(total_momentz)
    # total_momentx_df.to_csv("../res/total_momentz.csv")

    # second moment I
    moment_of_inertia_tranceverse = []
    moment_of_inertia_tranceverse = await calculate_moment_of_inertia(
        offset, moment_of_inertia_tranceverse, masscenter_x
    )
    print(len(moment_of_inertia_tranceverse))
    print(sum(moment_of_inertia_tranceverse))
    return offset_path


# 호출 부분
# result = await cal_run("./db/offset.csv")
# print("Function returned:", result)
