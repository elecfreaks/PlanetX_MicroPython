from microbit import *
import time

class ColorList:
    red = "red"
    green = "green"
    blue = "blue"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    white = "white"

# APDS-9960 I2C地址及寄存器定义
APDS9960_ADDR = 0x39
APDS9960_ENABLE = 0x80
APDS9960_ATIME = 0x81
APDS9960_CONTROL = 0x8F
APDS9960_STATUS = 0x93
APDS9960_CDATAL = 0x94
APDS9960_CDATAH = 0x95
APDS9960_RDATAL = 0x96
APDS9960_RDATAH = 0x97
APDS9960_GDATAL = 0x98
APDS9960_GDATAH = 0x99
APDS9960_BDATAL = 0x9A
APDS9960_BDATAH = 0x9B
APDS9960_GCONF4 = 0xAB
APDS9960_AICLEAR = 0xE7

# TCS3472 I2C地址及寄存器定义
TCS3472_ADDR = 0x43
class COLOR:
    """基本描述

    APDS9960, 颜色距离手势传感器，本文件只做颜色识别使用

    """

    def __init__(self):
        self.color_first_init = False
        self.color_new_init = False

    def i2c_write_color(self, addr, reg, value):
        buf = bytearray([reg, value])
        i2c.write(addr, buf)

    def i2c_read_color(self, addr, reg, length=1):
        i2c.write(addr, bytearray([reg]))
        return i2c.read(addr, length)[0]

    def read_16bit_data(self, addr, reg):
        low = self.i2c_read_color(addr, reg)
        high = self.i2c_read_color(addr, reg + 1)
        return (high << 8) | low

    def rgb2hsl(self, color_r, color_g, color_b):
        Hue = 0
        R = color_r * 100 / 255
        G = color_g * 100 / 255
        B = color_b * 100 / 255
        maxVal = max(R, G, B)
        minVal = min(R, G, B)
        Delta = maxVal - minVal

        if Delta < 0:
            Hue = 0
        elif maxVal == R and G >= B:
            Hue = (60 * ((G - B) * 100 / Delta)) / 100
        elif maxVal == R and G < B:
            Hue = (60 * ((G - B) * 100 / Delta) + 360 * 100) / 100
        elif maxVal == G:
            Hue = (60 * ((B - R) * 100 / Delta) + 120 * 100) / 100
        elif maxVal == B:
            Hue = (60 * ((R - G) * 100 / Delta) + 240 * 100) / 100
        return Hue

    def init_module(self):
        global color_first_init
        self.i2c_write_color(APDS9960_ADDR, APDS9960_ATIME, 0xFE)
        self.i2c_write_color(APDS9960_ADDR, APDS9960_CONTROL, 0x03)
        self.i2c_write_color(APDS9960_ADDR, APDS9960_ENABLE, 0x00)
        self.i2c_write_color(APDS9960_ADDR, APDS9960_GCONF4, 0x00)
        self.i2c_write_color(APDS9960_ADDR, APDS9960_AICLEAR, 0x00)
        self.i2c_write_color(APDS9960_ADDR, APDS9960_ENABLE, 0x01)
        self.color_first_init = True

    def colorMode(self):
        tmp = self.i2c_read_color(APDS9960_ADDR, APDS9960_ENABLE) | 0x2
        self.i2c_write_color(APDS9960_ADDR, APDS9960_ENABLE, tmp)

    def readColor(self):
        """

        读取当前颜色HUE值

        Returns:
            hue HUE颜色系统中的颜色,根据色环判断具体颜色
        """
        c = 0
        r = 0
        g = 0
        b = 0
        temp_c = 0
        temp_r = 0
        temp_g = 0
        temp_b = 0
        temp = 0

        if not self.color_first_init and not self.color_new_init:
            i = 0
            while i < 20:
                try:
                    i += 1
                    buf = bytearray([0x81, 0xCA])
                    i2c.write(TCS3472_ADDR, buf)
                    buf = bytearray([0x80, 0x17])
                    i2c.write(TCS3472_ADDR, buf)
                    time.sleep_ms(50)
        
                    if (self.i2c_read_color(TCS3472_ADDR, 0xA4) + self.i2c_read_color(TCS3472_ADDR, 0xA5) * 256) != 0:
                        self.color_new_init = True
                        break
                except:
                    continue

        if self.color_new_init:
            time.sleep_ms(100)
            c = self.i2c_read_color(TCS3472_ADDR, 0xA6) + self.i2c_read_color(TCS3472_ADDR, 0xA7) * 256
            r = self.i2c_read_color(TCS3472_ADDR, 0xA0) + self.i2c_read_color(TCS3472_ADDR, 0xA1) * 256
            g = self.i2c_read_color(TCS3472_ADDR, 0xA2) + self.i2c_read_color(TCS3472_ADDR, 0xA3) * 256
            b = self.i2c_read_color(TCS3472_ADDR, 0xA4) + self.i2c_read_color(TCS3472_ADDR, 0xA5) * 256

            r *= 0.50713
            g *= 0.320712
            b *= 0.27556
            c *= 0.3

            if r > b and r > g:
                b *= 1.18
                g *= 0.95

            temp_c = c
            temp_r = r
            temp_g = g
            temp_b = b

            r = min(r, 4095.9356)
            g = min(g, 4095.9356)
            b = min(b, 4095.9356)
            c = min(c, 4095.9356)

            if temp_b < temp_g:
                temp = temp_b
                temp_b = temp_g
                temp_g = temp

        else:
            if not self.color_first_init:
                self.init_module()
                self.colorMode()
            tmp = self.i2c_read_color(APDS9960_ADDR, APDS9960_STATUS) & 0x1
            while not tmp:
                sleep(5)
                tmp = self.i2c_read_color(APDS9960_ADDR, APDS9960_STATUS) & 0x1

            c = self.i2c_read_color(APDS9960_ADDR, APDS9960_CDATAL) + self.i2c_read_color(APDS9960_ADDR, APDS9960_CDATAH) * 256
            r = self.i2c_read_color(APDS9960_ADDR, APDS9960_RDATAL) + self.i2c_read_color(APDS9960_ADDR, APDS9960_RDATAH) * 256
            g = self.i2c_read_color(APDS9960_ADDR, APDS9960_GDATAL) + self.i2c_read_color(APDS9960_ADDR, APDS9960_GDATAH) * 256
            b = self.i2c_read_color(APDS9960_ADDR, APDS9960_BDATAL) + self.i2c_read_color(APDS9960_ADDR, APDS9960_BDATAH) * 256

        avg = c / 3
        r = r * 255 / avg
        g = g * 255 / avg
        b = b * 255 / avg
        hue = self.rgb2hsl(r, g, b)

        if self.color_new_init and hue >= 180 and hue <= 201 and temp_c >= 6000 and ((temp_b - temp_g) < 1000 or (temp_r > 4096 and temp_g > 4096 and temp_b > 4096)):
            temp_c = temp_c / 15000 * 13000
            hue = 180 + (13000 - temp_c) / 1000.0

        return hue

    def checkColor(self, color):
        hue = self.readColor()
        if color == ColorList.red:
            if hue > 330 or hue < 20:
                return True
            else:
                return False
        elif color == ColorList.green:
            if 120 < hue < 180:
                return True
            else:
                return False
        elif color == ColorList.blue:
            if 210 < hue < 270:
                return True
            else:
                return False
        elif color == ColorList.cyan:
            if 190 < hue < 210:
                return True
            else:
                return False
        elif color == ColorList.magenta:
            if 260 < hue < 330:
                return True
            else:
                return False
        elif color == ColorList.yellow:
            if 30 < hue < 120:
                return True
            else:
                return False
        elif color == ColorList.white:
            if 180 <= hue < 190:
                return True
            else:
                return False

# 使用示例
if __name__ == '__main__':
    i2c.init(freq=100000,sda=pin20,scl=pin19)
    color_sensor = COLOR()
    while True:
        hue = color_sensor.readColor()
        print("Detected HUE:", hue)
        is_red = color_sensor.checkColor(ColorList.red)
        print("Is Red:", is_red)
        sleep(1000)