import pandas as pd
import os
import random

def csv_to_bio(csv_path, output_dir):
    # 读取CSV文件，指定编码为GBK
    df = pd.read_csv(csv_path, encoding='GBK')

    # 创建单个输出文件
    output_file = os.path.join(output_dir, "风险防控BIO.txt")

    # 如果文件已存在，先删除它以避免追加到现有内容
    if os.path.exists(output_file):
        os.remove(output_file)

    # 定义10种不同的句式模板
    sentence_templates = [
        # 模板1
        lambda a, b, c, d: f"在{a}作业时，若存在{b}，可能引发{c}，需通过{d}进行有效预防",
        # 模板2
        lambda a, b, c, d: f"针对{a}的{b}问题，为避免{c}风险，必须严格执行{d}",
        # 模板3
        lambda a, b, c, d: f"{a}区域因{b}未被管控，易导致{c}，日常应落实{d}以消除隐患",
        # 模板4
        lambda a, b, c, d: f"为降低{a}中{b}引发的{c}概率，需优先实施{d}",
        # 模板5
        lambda a, b, c, d: f"若{a}的{b}未及时整改，可能升级为{c}，应通过{d}提前干预",
        # 模板6
        lambda a, b, c, d: f"在{a}排查时发现{b}，应立即采取{d}，防止{c}发生",
        # 模板7
        lambda a, b, c, d: f"{a}的{b}是{c}的主要诱因，需通过{d}从源头遏制风险",
        # 模板8
        lambda a, b, c, d: f"针对{a}高频出现的{b}，为防范{c}，需常态化执行{d}",
        # 模板9
        lambda a, b, c, d: f"{a}作业前，应对{b}进行全面检查，并落实{d}以规避{c}。",
        # 模板10
        lambda a, b, c, d: f"因{a}的{b}存在隐蔽性，需通过{d}主动预防，避免{c}突发"
    ]

    # 处理从第二行开始的每一行
    for i, row in df.iloc[1:].iterrows():
        # 提取各列的值
        col_A = row.iloc[0]  # 施工位置
        col_B = row.iloc[1]  # 危险源
        col_C = row.iloc[2]  # 潜在风险
        col_D = row.iloc[3]  # 预防措施

        # 随机选择一个句式模板
        template = random.choice(sentence_templates)

        # 使用选择的模板创建句子
        sentence = template(col_A, col_B, col_C, col_D)

        # 初始化每个字符的BIO标签
        bio_tags = ['O'] * len(sentence)

        # 处理A列的标签（施工位置）
        start_index = sentence.find(col_A)
        if start_index != -1:
            bio_tags[start_index] = 'B-施工位置'
            for j in range(start_index + 1, start_index + len(col_A)):
                bio_tags[j] = 'I-施工位置'

        # 处理B列的标签（危险源）
        start_index = sentence.find(col_B)
        if start_index != -1:
            bio_tags[start_index] = 'B-危险源'
            for j in range(start_index + 1, start_index + len(col_B)):
                bio_tags[j] = 'I-危险源'


        # 处理C列的标签（潜在风险）
        start_index = sentence.find(col_C)
        if start_index != -1:
            bio_tags[start_index] = 'B-潜在风险'
            for j in range(start_index + 1, start_index + len(col_C)):
                bio_tags[j] = 'I-潜在风险'


        # 处理列D标签（预防措施）
        # 前6个字符和最后一个字符标注为O，第7个字符标注为B-处置措施，其余为I-处置措施
        start_index = sentence.rfind(col_D)
        if start_index != -1 and len(col_D) > 4:
            bio_tags[start_index + 3] = 'B-预防措施'
            for j in range(start_index + 4, start_index + len(col_D) - 1):
                bio_tags[j] = 'I-预防措施'

        # 将结果写入到单一文件中
        with open(output_file, "a", encoding="utf-8") as f:
            for char, tag in zip(sentence, bio_tags):
                f.write(f"{char}\t{tag}\n")
            f.write("\n")  # 句子之间的空行


if __name__ == "__main__":
    csv_to_bio("风险防控.csv", "bio_output")
    print("转换完成。结果保存在 'bio_output/风险防控BIO.txt' 文件中。")
