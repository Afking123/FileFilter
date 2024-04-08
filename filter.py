import os

def filter_content(input_folder, output_file_extension):
    # 获取文件夹中所有文件的路径
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)]
    
    # 仅保留文件类型为.dxx的文件路径
    input_files = [f for f in input_files if f.endswith('.dxx')]

    for input_file in input_files:
        # 获取输入文件名（不含扩展名）
        input_filename = os.path.splitext(os.path.basename(input_file))[0]
        
        with open(input_file, 'r', encoding='utf-8') as f_input:
            lines = f_input.readlines()

        filtered_lines = []
        count_after_attribute = 0
        start_count = True
        statistics = {}

        for line in lines:
            if start_count:
                count_after_attribute = 0
                start_count = False

            if 'AcDbAttribute' in line:
                count_after_attribute = 0
            elif count_after_attribute < 2:
                # 仅保留以'D'、'W'、'SD' 开头的部分
                if line.strip().startswith(('D', 'W', 'SD')):
                    #filtered_lines.append(line.strip())
                    count_after_attribute += 1
                    key = line.strip().split()[0]  # 获取以 'D'、'W'、'SD' 开头的部分
                    statistics[key] = statistics.get(key, 0) + 1

        # 计算总共出现次数
        total_occurrences = sum(statistics.values())

        # 将统计结果添加到输出中
        statistics_output = "\n".join([f"{key} {value}個" for key, value in sorted(statistics.items())])
        statistics_output += f"\n\n總共出現{total_occurrences}次"
        filtered_lines.append("\n\n" + statistics_output)

        # 构建输出文件路径
        output_file_path = os.path.join(input_folder, f"{input_filename}.{output_file_extension}")

        # 将结果写入输出文件
        with open(output_file_path, 'w', encoding='utf-8') as f_output:
            f_output.write('\n'.join(filtered_lines))

        print(f"文件 {input_file} 筛选完成，结果已写入 {output_file_path}")

if __name__ == "__main__":
    input_folder =os.getcwd()  # 输入文件夹路径
    output_file_extension = "txt"  # 输出文件扩展名
    filter_content(input_folder, output_file_extension)