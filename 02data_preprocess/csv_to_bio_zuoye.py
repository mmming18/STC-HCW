import pandas as pd
import os
import random


def csv_to_bio(csv_path, output_dir):
    # 读取CSV文件，指定编码为GBK
    df = pd.read_csv(csv_path, encoding='GBK')

    # 创建单个输出文件
    output_file = os.path.join(output_dir, "作业控制BIO.txt")

    # 如果文件已存在，先删除它以避免追加到现有内容
    if os.path.exists(output_file):
        os.remove(output_file)

    # 定义5种不同的句式模板
    sentence_templates = [
        # 原始模板
        lambda a, b, c, d, e: f"对于{a}的{b}，在进行{c}的{d}工作时，{e}",
        # 新增模板1
        lambda a, b, c, d, e: f"在{b}施工区域的{a}，执行{c}{d}操作期间，需要{e}",
        # 新增模板2
        lambda a, b, c, d, e: f"{a}{b}区域内，当开展{c}的{d}施工环节时，应当{e}",
        # 新增模板3
        lambda a, b, c, d, e: f"针对{b}中的{a}，实施{c}{d}作业过程中，必须{e}",
        # 新增模板4
        lambda a, b, c, d, e: f"{a}和{b}位置，在{c}{d}施工阶段，要求{e}"
    ]

    # 处理从第二行开始的每一行
    for i, row in df.iloc[1:].iterrows():
        # 提取各列的值
        col_A = row.iloc[0]  # 施工位置
        col_B = row.iloc[1]  # 施工位置
        col_C = row.iloc[2]  # 施工活动
        col_D = row.iloc[3]  # 施工工序
        col_E = row.iloc[4]  # 作业要求

        # 随机选择一个句式模板
        template = random.choice(sentence_templates)

        # 使用选择的模板创建句子
        sentence = template(col_A, col_B, col_C, col_D, col_E)

        # 初始化每个字符的BIO标签
        bio_tags = ['O'] * len(sentence)

        # 处理A列和B列的标签（施工位置）
        # 查找所有col_A的出现位置
        pos = 0
        while True:
            start_index = sentence.find(col_A, pos)
            if start_index == -1:
                break
            bio_tags[start_index] = 'B-施工位置'
            for j in range(start_index + 1, start_index + len(col_A)):
                bio_tags[j] = 'I-施工位置'
            pos = start_index + 1

        # 查找所有col_B的出现位置
        pos = 0
        while True:
            start_index = sentence.find(col_B, pos)
            if start_index == -1:
                break
            bio_tags[start_index] = 'B-施工位置'
            for j in range(start_index + 1, start_index + len(col_B)):
                bio_tags[j] = 'I-施工位置'
            pos = start_index + 1

        # 处理C列的标签（施工活动）
        pos = 0
        while True:
            start_index = sentence.find(col_C, pos)
            if start_index == -1:
                break
            bio_tags[start_index] = 'B-施工活动'
            for j in range(start_index + 1, start_index + len(col_C)):
                bio_tags[j] = 'I-施工活动'
            pos = start_index + 1

        # 处理D列的标签（施工工序）
        pos = 0
        while True:
            start_index = sentence.find(col_D, pos)
            if start_index == -1:
                break
            bio_tags[start_index] = 'B-施工工序'
            for j in range(start_index + 1, start_index + len(col_D)):
                bio_tags[j] = 'I-施工工序'
            pos = start_index + 1

        # 处理E列的标签（作业要求）
        # 由于句式多样化，需要更精确地定位作业要求
        start_index = sentence.find(col_E)

        # 原始逻辑：前3个字符和最后一个字符标注为O，第4个字符标注为B-作业要求
        if len(col_E) > 4:
            bio_tags[start_index + 3] = 'B-作业要求'
            for j in range(start_index + 4, start_index + len(col_E) - 1):
                bio_tags[j] = 'I-作业要求'

        # 将结果写入到单一文件中
        with open(output_file, "a", encoding="utf-8") as f:
            for char, tag in zip(sentence, bio_tags):
                f.write(f"{char}\t{tag}\n")
            f.write("\n")  # 句子之间的空行


if __name__ == "__main__":
    csv_to_bio("作业控制.csv", "bio_output")
    print("转换完成。结果保存在 'bio_output/作业控制BIO.txt' 文件中。")
