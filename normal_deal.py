# 舍去小数位小于等于5的数，避免使用内置的 round 函数导致计算误差
import cv2


def round_but_in_five(becut):
    i = int(becut)  # 将浮点数转换为整数，自动舍去小数部分
    o = becut - i   # 计算小数部分
    if o <= 0.5:    # 比较小数部分是否小于等于 0.5
        final_number = int(becut)
    else:
        final_number = int(becut + 0.5)
    return final_number


# 用于计算红色值对应的坐标
def redcal(width_p, R):
    # 循环计算红色值，返回对应的坐标
    for i in range(256):
        re_cal = round_but_in_five((255 / width_p) * (0.5 + i))  # 四舍五入计算红色值
        if re_cal == R:  # 检查是否等于目标值
            return i


# 用于计算绿色值对应的坐标
def greencal(height_p, G):
    # 循环计算绿色值，返回对应的坐标
    for i in range(256):
        gr_cal = round_but_in_five((255 / height_p) * (0.5 + i))  # 四舍五入计算绿色值
        if gr_cal == G:  # 检查是否等于目标值
            return i


# 从坐标反推颜色 x
def redcal_re(plxt_re, long_re):
    # 根据公式直接计算红色值
    return round_but_in_five((255 / long_re) * (0.5 + plxt_re))


# 从坐标反推颜色 y
def greencal_re(plyt_gr, long_gr):
    # 根据公式直接计算绿色值
    return round_but_in_five((255 / long_gr) * (0.5 + plyt_gr))
