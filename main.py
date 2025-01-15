import shutil
import subprocess
import time
import cv2
import os
import numpy as np
from normal_deal import *

origin_file_folder = r"origin_files"
normal_file_folder = r"normal_files"
target_folder = r"final_files"
# 检查目标文件夹是否存在，如果不存在可以创建
if not os.path.exists(normal_file_folder):
    os.makedirs(normal_file_folder)
if not os.path.exists(target_folder):
    os.makedirs(target_folder)
# 定义三个通道的缩放系数
scale_factors = (140 / 225, 110 / 225, 88 / 225)  # 分别对应蓝、绿、红通道
palette_shape = (4, 256, 4)  # (高，宽，通道数)
fileName_list = sorted(os.listdir(origin_file_folder))
skinName_list = []
for name in fileName_list:
    if name[-5:] == "atlas":
        skinName_list.append(name[:-6])

print("所有皮肤：" + str(skinName_list))
skin_count = len(skinName_list)
print(f"预计耗时：{100 * skin_count / 60} 分钟")
skinGraphName_dict = {}
for key in skinName_list:
    skinGraphName_dict[key] = []

for name in fileName_list:
    if name[-4:] == ".png" and name[-5] != "s" and name[-5] != "n":
        for skinname in skinName_list:
            if name.find(skinname) > -1 and len(name) == len(skinname) + 5:
                skinGraphName_dict[skinname].append(name)
#######################################################################################################
err = []
count = 0
for skinname in skinGraphName_dict:
    print()
    start_time = time.time()
    count += 1
    print(f"当前皮肤：{skinname} ({count}/{skin_count}) 预计剩余时间{100 * (skin_count - count) / 60}分钟")
    print("复制 atlas 文件到中间文件夹：")
    try:
        altas_file_name = skinname + ".atlas"
        # 遍历并复制文件
        altas_file_path = os.path.join(origin_file_folder, altas_file_name)
        shutil.copy(altas_file_path, normal_file_folder)
        print(f"{altas_file_path} 已复制到 {normal_file_folder}")
    except Exception as e:
        print(f"\033[31m法复制文件: {e}\033[0m")
        err.append(skinname)
        continue
    ################################################################################################
    print(f"动作贴图共有: {skinGraphName_dict[skinname]}")


    skinPaletteName_list = []
    for name in fileName_list:
        if name[-6:] == "_s.png" and name.find(skinname) > -1 and name.find("placeholder") == -1 and name[len(skinname)] == "_":
            skinPaletteName_list.append(name)
    print("检测到所有的色带为：" + str(skinPaletteName_list))
    if len(skinPaletteName_list) > 0:
        skinpalette_path = os.path.join(origin_file_folder, skinPaletteName_list[0])
        if os.path.exists(skinpalette_path):
            skinpalette = cv2.imread(skinpalette_path, cv2.IMREAD_UNCHANGED)
            palette_shape = skinpalette.shape

        print("当前皮肤默认色带大小(高，宽，通道数)：", str(palette_shape))
    else:
        print("\033[31m未检测到色带文件！\033[0m", )
        err.append(skinname)
        continue

    print(f"生成 {skinname} 带有阴影的动作贴图中...")
    ###############################################################################################
    for skingraphname in skinGraphName_dict[skinname]:
        print(f"当前处理贴图：{skingraphname}")
        if os.path.isfile(os.path.join(normal_file_folder, skingraphname)):
            print(f"当前皮肤图片已被处理过！程序将跳过生成该图片，请考虑删除{normal_file_folder}内文件以重新生成！")
            continue

        skingraphname_n = skingraphname[:-4]+"_n.png"
        skingraph_path = os.path.join(origin_file_folder, skingraphname)
        skingraph_n_path = os.path.join(origin_file_folder, skingraphname_n)

        # [B, G, R, A]
        skingraph = cv2.imread(skingraph_path, cv2.IMREAD_UNCHANGED)
        # 获取绿色通道
        skingraph_G = skingraph[:, :, 1]

        # [B, G, R]
        skingraph_n = cv2.imread(skingraph_n_path)
        # img.shape
        # 返回：(高，宽，通道数)
        # 生成一张全透明图
        new_graph_G = np.zeros((skingraph.shape[0], skingraph.shape[1]), dtype=np.uint8)
        for i in range(skingraph.shape[0]):  # 第几行
            for j in range(skingraph.shape[1]):  # 第几列
                pixel_n = skingraph_n[i][j]
                if pixel_n[1] > pixel_n[2]:  # G > R，要加阴影
                    pixel_G = skingraph_G[i][j]
                    # x = redcal(palette_shape[1], pixel[2])
                    y = greencal(palette_shape[0], pixel_G)

                    y = y + palette_shape[0]
                    # new_red = redcal_re(x, palette_shape[1])
                    shadow_green = greencal_re(y, palette_shape[0] * 2)
                    # new_graph[i, j, 0] = 0  # 蓝色通道
                    new_graph_G[i, j] = shadow_green  # 绿色通道
                    # new_graph[i, j, 2] = pixel[1]  # 红色通道
                    # new_graph[i, j, 3] = 255  # 透明度通道（设置为不透明）
                    # new_graph[i][j] = np.array([0, new_green, new_red, 255])
                else:  # G < R ,更新绿色
                    pixel_G = skingraph_G[i][j]
                    if pixel_G == 0:  # 0直接跳过
                        continue
                    y = greencal(palette_shape[0], pixel_G)
                    new_green = greencal_re(y, palette_shape[0] * 2)
                    new_graph_G[i, j] = new_green  # 绿色通道

        skingraph[:, :, 1] = new_graph_G
        # 保存图像为PNG格式（支持透明度），你可以根据需要修改保存的文件名和路径
        cv2.imwrite(os.path.join(normal_file_folder, skingraphname), skingraph)

    print(f"贴图生成完毕，保存在 {normal_file_folder} 文件夹内")
    ################################################################################################
    print("接下来处理所有可检测到的色带")


    for palettename in skinPaletteName_list:
        print(f"当前处理色带：{palettename}")
        if os.path.isfile(os.path.join(target_folder, palettename)):
            print(f"当前色带图片已被处理过！程序将跳过生成该图片，请考虑删除{target_folder}内文件以重新生成！")
            continue

        palette_path = os.path.join(origin_file_folder, palettename)
        palettegraph = cv2.imread(palette_path, cv2.IMREAD_UNCHANGED)
        palette_shadow = palettegraph.copy()
        # for i in range(3):  # 遍历前三个通道（B, G, R）
        #     palette_shadow[:, :, i] = np.clip(palette_shadow[:, :, i] * scale_factors[i], 0, 255).astype(np.uint8)

        # 遍历每个像素
        for i in range(palette_shadow.shape[0]):
            for j in range(palette_shadow.shape[1]):
                # 提取当前像素的颜色
                pixel_color = palette_shadow[i, j, :3]  # 获取前三个通道 (B, G, R)

                # 如果颜色为 (255, 0, 0) 或 (255, 0, 255)，跳过处理
                if np.array_equal(pixel_color, [255, 0, 0]) or np.array_equal(pixel_color, [255, 0, 255]):
                    continue

                # 否则对每个通道应用缩放
                for k in range(3):  # 遍历前三个通道（B, G, R）
                    palette_shadow[i, j, k] = np.clip(palette_shadow[i, j, k] * scale_factors[k], 0, 255).astype(
                        np.uint8)


        # 拼接原图和处理后的图像
        palette_out = np.vstack((palettegraph, palette_shadow))
        # 保存图像为PNG格式（支持透明度），你可以根据需要修改保存的文件名和路径
        print("当前色带保存在：" + os.path.join(target_folder , palettename))
        cv2.imwrite(os.path.join(target_folder , palettename), palette_out)
    print(f"色带已处理完成！保存在 {target_folder} 文件夹中！")
    end_time = time.time()
    print("处理该皮肤共耗时：" + str(end_time - start_time) + "秒")
######################################################################################################

if len(err) > 0:
    print("出错文件：" + str(err))

print("执行动作贴图解包...")
ExpandAll = [
    'AtlasTool',
    '-ExpandAll',
    '-indir',
    r'.\normal_files',
    '-OutDir',
    r'.\expand_out'
]
subprocess.run(ExpandAll)
print("动作贴图解包完成！")

print("执行动作贴图打包：")
for Cskin in skinName_list:
    print("当前打包皮肤：" + Cskin)
    Collapse = [
        'AtlasTool',
        '-Collapse',
        '-indir',
        rf'.\expand_out\{Cskin}',
        '-Atlas',
        rf'.\collapse_out\{Cskin}.png',
        # '-ascii'
    ]
    subprocess.run(Collapse)
    print("打包完成！")

    # 定义源文件夹（文件夹A）和目标文件夹（文件夹B）的路径，你需要替换为实际的路径
    source_folder = r'collapse_out'

    # 获取源文件夹中的所有文件（不包含子文件夹中的文件，如果需要处理子文件夹中的文件，可以使用os.walk等方法进一步拓展）
    files = os.listdir(source_folder)

    for file in files:
        source_file_path = os.path.join(source_folder, file)
        target_file_path = os.path.join(target_folder, file)
        # 判断是否是文件（避免处理子文件夹等情况）
        if os.path.isfile(source_file_path):
            try:
                shutil.move(source_file_path, target_file_path)
                print(f"已成功将文件 {file} 从 {source_folder} 移动到 {target_folder}")
            except Exception as e:
                print(f"移动文件 {file} 时出现错误: {e}")

"""
"读取去色大图" \
"读取阴影" \
"遍历阴影图" \
"如果这个点需要添加阴影(r < g)" \
"计算这个点在色带上的横坐标，纵坐标" \
"计算纵坐标+4后对应的颜色" \
"将颜色涂到原始去色大图上"
print()
"""
