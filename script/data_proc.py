import math

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
                      2.0 * (self.qw*self.qw + self.qz*self.qz) - 1.0)

    def pitch_(self):
        return math.asin(max(-1.0, min(1.0, 2.0 * (self.qw * self.qx + self.qy * self.qz))))
    
    def yaw_(self):
        return math.atan2(2.0 * (self.qw * self.qz - self.qx * self.qy),
                     2.0 * (self.qw*self.qw + self.qy*self.qy) - 1.0)