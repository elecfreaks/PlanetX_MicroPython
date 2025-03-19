from microbit import i2c, sleep

class TrackbitStateType:
    Tracking_State_0 = 0  # ◌ ◌ ◌ ◌
    Tracking_State_1 = 6  # ◌ ● ● ◌
    Tracking_State_2 = 4  # ◌ ◌ ● ◌
    Tracking_State_3 = 2  # ◌ ● ◌ ◌
    Tracking_State_4 = 9  # ● ◌ ◌ ●
    Tracking_State_5 = 15 # ● ● ● ●
    Tracking_State_6 = 13 # ● ◌ ● ●
    Tracking_State_7 = 11 # ● ● ◌ ●
    Tracking_State_8 = 1  # ● ◌ ◌ ◌
    Tracking_State_9 = 7  # ● ● ● ◌
    Tracking_State_10 = 5 # ● ◌ ● ◌
    Tracking_State_11 = 3 # ● ● ◌ ◌
    Tracking_State_12 = 8 # ◌ ◌ ◌ ●
    Tracking_State_13 = 14# ◌ ● ● ●
    Tracking_State_14 = 12# ◌ ◌ ● ●
    Tracking_State_15 = 10# ◌ ● ◌ ●

class TrackbitChannel:
    One = 0
    Two = 1
    Three = 2
    Four = 3

class TrackbitType:
    State_0 = 0  # ◌
    State_1 = 1  # ●

class FourWayTrackBit:
    """基本描述

    四路巡线模块 IIC驱动类

    """
    def __init__(self, device_addr=0x1a):
        self.DEVICE_ADDR = device_addr
        self.TrackBit_state_value = 0

    def TrackbitgetGray(self, channel):
        """获取通道的灰度值，范围从0到255"""
        i2c.write(self.DEVICE_ADDR, bytes([channel]), repeat=False)
        gray_value = i2c.read(self.DEVICE_ADDR, 1)[0]
        return gray_value

    def TrackbitState(self, State):
        """检查Trackbit的状态是否等于给定状态"""
        self.Trackbit_get_state_value()
        return self.TrackBit_state_value == State

    def TrackbitChannelState(self, channel, state):
        """检查指定通道的状态"""
        i2c.write(self.DEVICE_ADDR, bytes([4]), repeat=False)
        TempVal = i2c.read(self.DEVICE_ADDR, 1)[0]
        if state == TrackbitType.State_1:  # 假设TrackbitType.State_1对应于数值1
            return bool(TempVal & (1 << channel))
        else:
            return not bool(TempVal & (1 << channel))

    def TrackBit_get_offset(self):
        """获取位置偏移，范围从-3000到3000"""
        i2c.write(self.DEVICE_ADDR, bytes([5]), repeat=False)
        offsetH = i2c.read(self.DEVICE_ADDR, 1)[0]
        i2c.write(self.DEVICE_ADDR, bytes([6]), repeat=False)
        offsetL = i2c.read(self.DEVICE_ADDR, 1)[0]
        offset = (offsetH << 8) | offsetL
        offset = int(offset / 6000.0 * 6000 - 3000)
        return offset

    def Trackbit_get_state_value(self):
        """获取Trackbit状态值"""
        i2c.write(self.DEVICE_ADDR, bytes([4]), repeat=False)
        self.TrackBit_state_value = i2c.read(self.DEVICE_ADDR, 1)[0]
        sleep(5)

# 使用示例
if __name__ == '__main__':
    trackbit = FourWayTrackBit()
    while True:
        print(trackbit.TrackbitgetGray(TrackbitChannel.One))  # 示例：获取通道1的灰度值
        print(trackbit.TrackBit_get_offset())  # 示例：获取偏移值
        if trackbit.TrackbitState(TrackbitStateType.Tracking_State_1):
            print("当前状态匹配Tracking_State_1")
        if trackbit.TrackbitChannelState(TrackbitChannel.One,TrackbitType.State_0):
            print("当前状态匹配TrackbitType.State_0")
        sleep(100)