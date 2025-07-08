import os
import glob


def clean_bio_files(directory_path, output_directory=None):
    """
    清理BIO文件，只保留格式正确的行（每行有且只有两列），删除其他行

    Args:
        directory_path: 包含BIO文件的目录路径
        output_directory: 清理后文件的输出目录，默认为None（创建新目录）
    """
    # 确保目录路径以斜杠结尾
    if not directory_path.endswith('/'):
        directory_path += '/'

    # 设置输出目录
    if output_directory is None:
        output_directory = directory_path + 'cleaned/'
    elif not output_directory.endswith('/'):
        output_directory += '/'

    # 创建输出目录
    os.makedirs(output_directory, exist_ok=True)

    # 获取所有txt文件
    files = glob.glob(directory_path + "*.txt")
    print(f"找到 {len(files)} 个文件进行清理")

    cleaned_files = 0
    removed_lines = 0

    for file_path in files:
        file_name = os.path.basename(file_path)
        cleaned_content = []
        file_had_issues = False

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            line_count = len(lines)

            for line_num, line in enumerate(lines, 1):
                # 处理空行 - 保留
                if line.strip() == '':
                    cleaned_content.append(line)
                    continue

                # 分割行
                fields = line.strip().split('\t')

                # 只保留正确的行（有且只有两列）
                if len(fields) == 2:
                    cleaned_content.append(line)
                else:
                    removed_lines += 1
                    file_had_issues = True
                    print(f"文件 {file_name} 行 {line_num}: 发现 {len(fields)} 列，已删除")

        # 写入清理后的内容
        output_path = os.path.join(output_directory, file_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_content)

        if file_had_issues:
            cleaned_files += 1
            print(f"已清理文件: {file_name}")

    print(
        f"\n清理完成！处理了 {len(files)} 个文件，修改了 {cleaned_files} 个文件，共删除 {removed_lines} 行不符合格式的内容")
    print(f"清理后的文件保存在: {output_directory}")


def count_columns_in_file(file_path):
    """
    统计文件中每行的列数，生成报告

    Args:
        file_path: 文件路径
    """
    column_counts = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            # 跳过空行
            if line.strip() == '':
                continue

            # 分割行
            fields = line.strip().split('\t')
            cols = len(fields)

            if cols not in column_counts:
                column_counts[cols] = 0
            column_counts[cols] += 1

    print(f"\n文件 {os.path.basename(file_path)} 的列统计:")
    for cols, count in sorted(column_counts.items()):
        print(f"  {cols} 列的行数: {count}")


# 使用示例
if __name__ == "__main__":
    # 替换为你的BIO文件目录
    BIO_DIRECTORY = "./txt_spilt/"
    OUTPUT_DIRECTORY = "./txt_spilt2/"

    # 清理文件
    clean_bio_files(BIO_DIRECTORY, OUTPUT_DIRECTORY)

    # 检查清理后的文件
    print("\n验证清理后的文件:")
    cleaned_files = glob.glob(OUTPUT_DIRECTORY + "*.txt")

    if cleaned_files:
        for file_path in cleaned_files[:3]:  # 只检查前3个文件
            count_columns_in_file(file_path)