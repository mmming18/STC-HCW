import pandas as pd
import os
import random

def csv_to_bio(csv_path, output_dir):
    # 读取CSV文件，指定编码为GBK
    df = pd.read_csv(csv_path, encoding='GBK')

    # 创建单个输出文件
    output_file = os.path.join(output_dir, "应急处置BIO.txt")

    # 如果文件已存在，先删除它以避免追加到现有内容
    if os.path.exists(output_file):
        os.remove(output_file)

    # 定义10种不同的句式模板
    sentence_templates = [
        # 模板1
        lambda a, b, c, d, e: f"在{a}的{b}区域，因{c}可能引发{d}时，应立即{e}",
        # 模板2
        lambda a, b, c, d, e: f"针对{a}中存在的{b}，为避免{c}升级为{d}，需严格执行{e}",
        # 模板3
        lambda a, b, c, d, e: f"若{a}的{b}未被有效管控，将导致{c}并触发{d}，此时应迅速{e}",
        # 模板4
        lambda a, b, c, d, e: f"{a}内因{b}产生的{c}，一旦发展为{d}，必须优先采取{e}",
        # 模板5
        lambda a, b, c, d, e: f"为预防{a}的{b}引发{c}及{d}，作业前应落实{e}",
        # 模板6
        lambda a, b, c, d, e: f"当{a}发生{b}相关的{c}并出现{d}时，需按预案{e}",
        # 模板7
        lambda a, b, c, d, e: f"{a}中{b}若未及时处理，可能因{c}造成{d}，需立即{e}",
        # 模板8
        lambda a, b, c, d, e: f"在{a}排查{b}时，若发现{c}可能导致{d}，应提前部署{e}",
        # 模板9
        lambda a, b, c, d, e: f"{a}的{b}管理失控会加剧{c}，最终引发{d}，此时需紧急{e}",
        # 模板10
        lambda a, b, c, d, e: f"针对{a}内{b}导致的{c}和{d}，必须按照{e}开展救援"
    ]

    # 处理从第二行开始的每一行
    for i, row in df.iloc[1:].iterrows():
        # 提取各列的值
        col_A = row.iloc[0]  # 施工位置
        col_B = row.iloc[1]  # 危险源
        col_C = row.iloc[2]  # 潜在风险
        col_D = row.iloc[3]  # 事故类型
        col_E = row.iloc[4]  # 处置措施

        # 随机选择一个句式模板
        template = random.choice(sentence_templates)

        # 使用选择的模板创建句子
        sentence = template(col_A, col_B, col_C, col_D, col_E)

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

        # 处理D列的标签（事故类型）
        start_index = sentence.find(col_D)
        if start_index != -1:
            bio_tags[start_index] = 'B-事故类型'
            for j in range(start_index + 1, start_index + len(col_D)):
                bio_tags[j] = 'I-事故类型'

        # 处理E列的标签（处置措施）
        # 前3个字符和最后一个字符标注为O，第4个字符标注为B-处置措施，其余为I-处置措施
        start_index = sentence.rfind(col_E)
        if start_index != -1 and len(col_E) > 4:
            bio_tags[start_index + 3] = 'B-处置措施'
            for j in range(start_index + 4, start_index + len(col_E) - 1):
                bio_tags[j] = 'I-处置措施'

        # 将结果写入到单一文件中
        with open(output_file, "a", encoding="utf-8") as f:
            for char, tag in zip(sentence, bio_tags):
                f.write(f"{char}\t{tag}\n")
            f.write("\n")  # 句子之间的空行


if __name__ == "__main__":
    csv_to_bio("应急处置.csv", "bio_output")
    print("转换完成。结果保存在 'bio_output/应急处置BIO.txt' 文件中。")
