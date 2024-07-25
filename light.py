from microbit import *
from enum import *


class LIGHT(object):
    """基本描述

    环境光传感器，返回lux

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: 光线强度 0-16000lux
    """

    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            self.__pin = pin1
        elif RJ_pin == J2:
            self.__pin = pin2

    def get_lightlevel(self):
        """基本描述

        环境光传感器，返回lux

        Returns:
            value: 光强度单位勒克司Lux
        """
        raw_value = self.__pin.read_analog()

        # 为确保结果非负，我们可以直接处理不同区间的线性映射
        if raw_value <= 200:
            # 对原始区间[45, 200]进行映射到[0, 1600]
            lux = (raw_value - 45) * (1600 / (200 - 45))
        else:
            # 对原始区间[201, 1023]进行映射到[1600, 14000]
            lux = 1600 + (raw_value - 200) * ((14000 - 1600) / (1023 - 200))

        return max(0, lux) 

if __name__ == "__main__":
    s = LIGHT(J1)
    while True:
        print(s.get_lightlevel())
