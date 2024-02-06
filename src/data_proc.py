import json
import math


def NormalizeAngle(angle):
    a = math.fmod(angle + math.pi, 2.0 * math.pi)
    if a < 0.0:
        a += (2.0 * math.pi)
    return a - math.pi


heading = list()


def read_json(pth: str):
    fp = open(pth, 'r')
    data = json.load(fp)
    for d in data:
        dd = d['msg']['pose']['pose']['orientation']
        e = EulerAnglesZXY(dd['w'], dd['x'], dd['y'], dd['z'])
        hd = e.quaternionToHeading()
        if hd in heading:
            continue
        heading.append(e.quaternionToHeading())
        # print(e.quaternionToHeading())


class EulerAnglesZXY:
    def __init__(self, qw, qx, qy, qz) -> None:
        self.qw = qw
        self.qx = qx
        self.qy = qy
        self.qz = qz
        self.roll = self.roll_()
        self.pitch = self.pitch_()
        self.yaw = self.yaw_()

    def roll_(self):
        return math.atan2(2.0 * (self.qw * self.qy - self.qx * self.qz),
                          2.0 * (self.qw * self.qw + self.qz * self.qz) - 1.0)

    def pitch_(self):
        return math.asin(max(-1.0, min(1.0, 2.0 * (self.qw * self.qx + self.qy * self.qz))))

    def yaw_(self):
        return math.atan2(2.0 * (self.qw * self.qz - self.qx * self.qy),
                          2.0 * (self.qw * self.qw + self.qy * self.qy) - 1.0)

    def quaternionToHeading(self) -> float:
        return NormalizeAngle(self.yaw + math.pi / 2)


read_json(r"C:\Users\Lori-\Downloads\localization_1.json")
for e in heading:
    print(e)
