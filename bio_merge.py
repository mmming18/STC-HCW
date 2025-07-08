import os
from pathlib import Path

def merge_bio_files(input_dir, output_file, sentence_separator='\n'):
    # 确保输出目录存在
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 获取输入目录中的所有txt文件
    bio_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    bio_files.sort()  # 按文件名排序

    print(f"找到{len(bio_files)}个BIO文件")

    # 合并文件内容
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, bio_file in enumerate(bio_files):
            file_path = os.path.join(input_dir, bio_file)
            print(f"正在处理 ({i + 1}/{len(bio_files)}): {bio_file}")

            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read().rstrip()

                # 添加文件内容到输出文件
                if i > 0:  # 不是第一个文件，添加句子分隔符
                    outfile.write(sentence_separator)

                outfile.write(content)

    print(f"合并完成! 输出文件: {output_file}")

input_directory = "dev"  # <-- 修改这里为您的输入目录
output_filepath = "dev.txt"  # <-- 修改这里为您的输出文件路径

# 不同句子/文档之间的分隔符，通常BIO格式使用空行来分隔不同句子
# 可以根据需要修改，例如：'\n'表示一个空行分隔不同句子
sentence_separator = '\n'

# 执行合并操作
merge_bio_files(input_directory, output_filepath, sentence_separator)

print("脚本执行完毕!")