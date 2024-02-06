import json
import math


def read_json(path: str):
    fp = open(path, 'r', encoding='utf-8')
    dt = json.load(fp)
    return dt


threshold = 0.003


def compare_(fn1, fn2):
    max_ = max(fn1, fn2)
    min_ = min(fn1, fn2)
    if min_ == 0 or max_ == 0:
        return abs(max_ - min_) <= 1e-9
    return abs(max_ - min_) / abs(min_) <= threshold


dt1 = read_json("./scenario_rec/ces2024_wo_obs_1/trajectory.json")
dt2 = read_json("./scenario_rec/ces2024_wo_obs_2/trajectory.json")

# assert len(dt1) == len(dt2)
# print(len(dt1), len(dt2))
lines = 0

d1 = dt1[15]['msg']['points']
d2 = dt2[15]['msg']['points']

print(len(d1), len(d2), threshold)

for i in range(len(d1)):
    print(i)
    # print(d1[i]['pose']['position']['x'], d2[i]['pose']['position']['x'])
    assert compare_(d1[i]['pose']['position']['x'], d2[i]['pose']['position']['x'])
    assert compare_(d1[i]['pose']['position']['y'], d2[i]['pose']['position']['y'])
    assert compare_(d1[i]['pose']['position']['z'], d2[i]['pose']['position']['z'])
    assert compare_(d1[i]['pose']['orientation']['x'], d2[i]['pose']['orientation']['x'])
    assert compare_(d1[i]['pose']['orientation']['y'], d2[i]['pose']['orientation']['y'])
    assert compare_(d1[i]['pose']['orientation']['z'], d2[i]['pose']['orientation']['z'])
    assert compare_(d1[i]['pose']['orientation']['w'], d2[i]['pose']['orientation']['w'])
    assert compare_(d1[i]['longitudinal_velocity_mps'], d2[i]['longitudinal_velocity_mps'])
    assert compare_(d1[i]['lateral_velocity_mps'], d2[i]['lateral_velocity_mps'])
    assert compare_(d1[i]['heading_rate_rps'], d2[i]['heading_rate_rps'])
    assert compare_(d1[i]['acceleration_mps2'], d2[i]['acceleration_mps2'])
    assert compare_(d1[i]['front_wheel_angle_rad'], d2[i]['front_wheel_angle_rad'])
    assert compare_(d1[i]['rear_wheel_angle_rad'], d2[i]['rear_wheel_angle_rad'])

# for i in range(len(dt1)):
#     print(i)
#     # assert len(dt1[i]['msg']['points']) == len(dt2[i]['msg']['points'])
#     # print(len(dt1[i]['msg']['points']) )
#     lines += len(dt1[i]['msg']['points']) * 25 + 2
#     # print(lines)
#     dtt1 = dt1[i]['msg']['points']
#     dtt2 = dt2[i]['msg']['points']

#     for j in range(len(dtt1)):
#         assert dtt1[j] == dtt2[j]

