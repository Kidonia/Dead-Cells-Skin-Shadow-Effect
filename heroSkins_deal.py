import os
import shutil
import subprocess

folder_path = r'expand_out'
target_folder = r'heroSkins'
idlename = ['idle_00-=-0-=-.png', 'idle_01-=-0-=-.png', 'idle_02-=-0-=-.png', 'idle_03-=-0-=-.png', 'idle_04-=-0-=-.png', 'idle_05-=-0-=-.png', 'idle_06-=-0-=-.png', 'idle_07-=-0-=-.png', 'idle_08-=-0-=-.png', 'idle_09-=-0-=-.png', 'idle_10-=-0-=-.png', 'idle_11-=-0-=-.png', 'idle_12-=-0-=-.png', 'idle_13-=-0-=-.png', 'idle_14-=-0-=-.png', 'idle_15-=-0-=-.png', 'idle_16-=-0-=-.png', 'idle_17-=-0-=-.png', 'idle_18-=-0-=-.png', 'idle_19-=-0-=-.png', 'idle_20-=-0-=-.png', 'idle_21-=-0-=-.png', 'idle_22-=-0-=-.png', 'idle_23-=-0-=-.png', 'idle_24-=-0-=-.png', 'idle_25-=-0-=-.png', 'idle_26-=-0-=-.png', 'idle_27-=-0-=-.png', 'idle_28-=-0-=-.png', 'idle_29-=-0-=-.png', 'idle_30-=-0-=-.png', 'idle_31-=-0-=-.png', 'idle_32-=-0-=-.png', 'idle_33-=-0-=-.png', 'idle_34-=-0-=-.png', 'idle_35-=-0-=-.png', 'idle_36-=-0-=-.png', 'idle_37-=-0-=-.png', 'idle_38-=-0-=-.png', 'idle_39-=-0-=-.png', 'idle_40-=-0-=-.png', 'idle_41-=-0-=-.png', 'idle_42-=-0-=-.png', 'idle_43-=-0-=-.png', 'idle_44-=-0-=-.png', 'idle_45-=-0-=-.png']
folder_names_list = os.listdir(folder_path)
total_anim_list = []
target_anim_list = []

for folder_name in folder_names_list:
    skin_path = os.path.join(folder_path, folder_name)

    for idle in idlename:
        idle_path = os.path.join(skin_path, idle)

        target_path = os.path.join(target_folder, folder_name+"_"+idle)
        total_anim_list.append(idle_path)
        target_anim_list.append(target_path)


print(total_anim_list)
print(target_anim_list)

for i in range(len(total_anim_list)):
    source_file_path = total_anim_list[i]
    target_file_path = target_anim_list[i]
    # 判断是否是文件（避免处理子文件夹等情况）
    if os.path.isfile(source_file_path):
        try:
            # shutil.move(source_file_path, target_file_path)
            shutil.copy(source_file_path, target_file_path)
            # print(f"已成功移动{source_file_path}")
        except Exception as e:
            print(f"移动{source_file_path}时出现错误: {e}")


Collapse_heroSkins = [
        'AtlasTool',
        '-Collapse',
        '-indir',
        rf'.\pythonProject2\heroSkins',
        '-Atlas',
        rf'.\pythonProject2\collapse_out\heroSkins.png',
        # '-ascii'
        ]
subprocess.run(Collapse_heroSkins)
print("打包完成！")
# 定义源文件夹（文件夹A）和目标文件夹（文件夹B）的路径，你需要替换为实际的路径
source_folder = r'collapse_out'

# 获取源文件夹中的所有文件（不包含子文件夹中的文件，如果需要处理子文件夹中的文件，可以使用os.walk等方法进一步拓展）
files = os.listdir(source_folder)
for file in files:
    source_file_path = os.path.join(source_folder, file)
    target_file_path = os.path.join(r"final_files", file)
    # 判断是否是文件（避免处理子文件夹等情况）
    if os.path.isfile(source_file_path):
        try:
            shutil.move(source_file_path, target_file_path)
            print(f"已成功将文件 {file} 从 {source_folder} 移动到 final_files")
        except Exception as e:
            print(f"移动文件 {file} 时出现错误: {e}")