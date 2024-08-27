import os

# 基本的 WSL 命令结构
base_command = 'C:\\Windows\\system32\\wsl.exe --distribution Ubuntu --exec /bin/bash -c "cd /mnt/d/A_xmj/2022-2025/graduatepaper/libMultiRobotPlanning-main/libMultiRobotPlanning-main/build && /mnt/d/A_xmj/2022-2025/graduatepaper/libMultiRobotPlanning-main/libMultiRobotPlanning-main/build/cbs ./cbs'

# 设置输入和输出目录
input_dir = "../benchmark/32x32_obst204"
output_dir = "../benchmark/changed_output"
# output_dir = "../benchmark/original_output"
txt_output_path = "../benchmark/command-line.txt"

# 转换路径为 WSL 格式
input_dir_wsl = input_dir.replace("D:", "/mnt/d").replace("\\", "/")
output_dir_wsl = output_dir.replace("D:", "/mnt/d").replace("\\", "/")

# 生成命令行并写入文件
with open(txt_output_path, 'w') as file:
    # 遍历文件夹中的所有文件
    for input_file in os.listdir(input_dir):
        # 确保是文件而不是目录
        if os.path.isfile(os.path.join(input_dir, input_file)):
            # 生成输出文件名，加上 'output_' 前缀
            output_file = "output_" + input_file
            # 构造完整的命令行
            command_line = f'{base_command} -i {input_dir_wsl}/{input_file} -o {output_dir_wsl}/{output_file} python3 ../example/visualize.py {input_dir_wsl}/{input_file} {output_dir_wsl}/{output_file}"'
            # 写入文件
            file.write(command_line + "\n")

# 打印完成消息
print("Command lines written to", txt_output_path)
