import yaml
import os


# 读取YAML文件
def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def caculate_a_agent_turns(agent, path):
    turns = 0
    # 初始化上一个位置
    prev_pos = path[0]
    # 初始化上一个方向, 设 2: up, 3: down, 4: left, 5: right
    prev_direction = None
    # 初始化转向次数
    turn_count = 0

    # 遍历路径中的每个位置
    for pos in path:
        # 计算当前位置和上一个位置之间的方向
        direction = None
        if prev_pos!= None:
            dx = pos['x'] - prev_pos['x']
            dy = pos['y'] - prev_pos['y']
            if dx == 0 and dy == 1:
                direction = 2
            elif dx == 0 and dy == -1:
                direction = 3
            elif dx == 1 and dy == 0:
                direction = 5
            elif dx == -1 and dy == 0:
                direction = 4

        if prev_direction != None:
            if prev_direction != direction:
                turns += 1
        prev_direction = direction
        prev_pos = pos
    return turns

# 计算转向次数
def calculate_turns(schedule):
    agent_turns = []
    total_turns = 0
    agent_id = 0
    for agent, path in schedule.items():
        turns = caculate_a_agent_turns(agent, path)
        agent_turns.append(f"Agent {agent_id} turnCount={turns}")
        total_turns += turns
        agent_id += 1
    results = [f"turnCount={total_turns}"] + agent_turns
    return results

def write_results_to_file(results, output_file_path):
    with open(output_file_path, 'w') as file:
        for line in results:
            file.write(line + '\n')


def run(file_dir, output_file_dir):
    for input_file in os.listdir(file_dir):
        if os.path.isfile(os.path.join(file_dir, input_file)):
            output_file_path = output_file_dir + "output" + input_file
            data = read_yaml_file(file_dir + input_file)
            schedule = data['schedule']
            result = calculate_turns(schedule)
            write_results_to_file(result, output_file_path)

# 主函数
def main():
    original_file_dir = '../benchmark/original_output/'
    changed_file_dir = '../benchmark/changed_output/'
    output_original_file_dir = '../benchmark/results_original/'
    output_changed_file_dir = '../benchmark/results_changed/'

    run(original_file_dir, output_original_file_dir)

    run(changed_file_dir, output_changed_file_dir)

    files_original = [f for f in os.listdir(output_original_file_dir) if f.endswith('.yaml')]

    # 打开用于写入比较结果的文件
    with open('../benchmark/compare_results.txt', 'w') as result_file:
        for file_name in files_original:
            # 构造文件夹A和B中文件的完整路径
            file_path_ori = os.path.join(output_original_file_dir, file_name)
            file_path_cha = os.path.join(output_changed_file_dir, file_name)

            # 检查文件夹B是否有相同名称的文件
            if os.path.exists(file_path_cha):
                # 打开文件夹A中的文件并读取第一行
                with open(file_path_ori, 'r') as file_a:
                    line_a = file_a.readline().strip()
                    original = int(line_a.split('=')[1])  # 从等号后面提取数字

                # 打开文件夹B中的文件并读取第一行
                with open(file_path_cha, 'r') as file_b:
                    line_b = file_b.readline().strip()
                    changed = int(line_b.split('=')[1])  # 从等号后面提取数字

                # 计算两个数字之差
                compared = original - changed

                # 将结果写入compare_results.txt
                result_file.write(
                    f"{file_name}        original={original}    changed={changed}        compared={compared}\n")
            else:
                print(f"File {file_name} not found in folder B.")

    print("Comparison is complete, results are written in compare_results.txt")


if __name__ == "__main__":
    main()