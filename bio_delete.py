import os
import shutil
from pathlib import Path


def process_bio_files(input_folder, output_folder):
    """
    处理输入文件夹中的所有bio标注文件，删除指定标签的行，并保存到输出文件夹

    Args:
        input_folder: 包含原始bio标注文件的文件夹路径
        output_folder: 保存处理后文件的文件夹路径
    """
    # 要删除的标签列表
    labels_to_remove = [
        "I-预防措施",
        "I-处置措施",
        "I-作业要求",
        "B-预防措施",
        "B-处置措施",
        "B-作业要求"
    ]

    # 确保输出文件夹存在
    output_path = Path(output_folder)
    if not output_path.exists():
        output_path.mkdir(parents=True)

    # 获取输入文件夹中的所有文件
    input_path = Path(input_folder)
    file_count = 0
    removed_lines_count = 0

    for file_path in input_path.iterdir():
        if file_path.is_file():
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 过滤掉包含指定标签的行
            filtered_lines = []
            for line in lines:
                line = line.strip()
                # 跳过空行
                if not line:
                    filtered_lines.append('\n')
                    continue

                # 检查行是否包含要删除的标签
                parts = line.split()
                if len(parts) >= 2 and parts[-1] in labels_to_remove:
                    removed_lines_count += 1
                    continue

                filtered_lines.append(line + '\n')

            # 将处理后的内容写入新文件
            output_file_path = output_path / file_path.name
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)

            file_count += 1

    print(f"处理完成！共处理了 {file_count} 个文件，删除了 {removed_lines_count} 行内容。")


if __name__ == "__main__":
    # 在这里设置输入和输出文件夹的路径
    input_folder = "./txt_spilt2"  # 请替换为实际的输入文件夹路径
    output_folder = "./txt_spilt3"  # 请替换为实际的输出文件夹路径

    process_bio_files(input_folder, output_folder)