import pandas as pd
import random
import json
import re


# 读取Excel文件数据
def read_excel_data(file_path):
    """读取Excel文件数据"""
    try:
        df = pd.read_excel(file_path)
        # 重命名列为A, B, C, D便于处理
        if len(df.columns) >= 4:
            df.columns = ['A', 'B', 'C', 'D'] + list(df.columns[4:])
        return df
    except Exception as e:
        print(f"读取Excel文件出错: {e}")
        print("使用示例数据...")
        # 使用您提供的示例数据
        data = {
            'A': ['危险源'] + ['基坑开挖作业'] * 19,
            'B': ['潜在风险'] + ['坍塌倾覆风险'] * 9 + ['高处坠落风险'] * 10,
            'C': ['事故类型'] + ['坍塌倾覆事故'] * 9 + ['高处坠落事故'] * 10,
            'D': ['处置措施'] + [
                '事故发生后，立即拨打120急救电话，并通知现场负责人',
                '断开电源，并消除周边危险因素，拉设警戒线',
                '立即撤出危险区域的人员和设备，在保证安全的情况下积极展开救援',
                '在施救过程中，支护体系必须做好加固措施，严禁用机械设备直接救援，应保证救援人员及伤者的安全',
                '及时安顿好伤者并展开急救，进行包扎和止血',
                '四肢小动脉静脉出血，可用指压直线法进行止血',
                '四肢大血管出血，尤其是动脉出血，应用止血带进行止血',
                '止血带不宜直接与伤员的皮肤接触，需要垫上衣服或棉花纱布等，一般扎在伤口近心端，对于四肢出血的情况一般扎在上臂或者大腿的1/3处为宜',
                '包扎时先对创伤处消毒清洗再用纱布覆盖用绷带或干净的布条包扎',
                '安排专人，送医院并与急救部门保持联系，或在路口迎接急救车辆并耐心等待救援'
            ] + ['事故发生后，立即拨打120急救电话，并报告现场负责人'] * 10
        }
        return pd.DataFrame(data)


# 生成多样化的句式模板
def get_sentence_templates():
    """返回10种不同的句式模板"""
    templates = [
        "在{A}过程中，可能出现{B}，进而导致{C}的发生，此时需要采取{D}来应对。",
        "当进行{A}时，由于存在{B}，容易引发{C}，因此必须实施{D}。",
        "针对{A}活动，其潜在的{B}会造成{C}，相应的{D}应当及时执行。",
        "在{A}操作中，{B}的存在可能引起{C}，为此需要落实{D}措施。",
        "对于{A}作业，{B}是主要威胁，可能导致{C}，故应采用{D}进行处置。",
        "实施{A}时，面临{B}的挑战，这会产生{C}的后果，需通过{D}来解决。",
        "在{A}环节，{B}构成安全隐患，易造成{C}，必须通过{D}加以控制。",
        "开展{A}工作过程中，{B}的威胁不容忽视，可能发生{C}，应当执行{D}。",
        "执行{A}任务时，{B}是关键风险点，会引发{C}，需要运用{D}进行防范。",
        "进行{A}施工中，{B}带来的安全威胁会导致{C}，此时{D}显得尤为重要。"
    ]
    return templates


# 任务1：生成段落
def generate_paragraphs(df):
    """生成段落文本"""
    templates = get_sentence_templates()
    paragraphs = []

    for i in range(1, len(df)):
        # 随机选择一个句式模板
        template = random.choice(templates)

        # 提取当前行的数据
        row_data = {
            'A': df.iloc[i]['A'] if pd.notna(df.iloc[i]['A']) else '作业活动',
            'B': df.iloc[i]['B'] if pd.notna(df.iloc[i]['B']) else '安全风险',
            'C': df.iloc[i]['C'] if pd.notna(df.iloc[i]['C']) else '安全事故',
            'D': df.iloc[i]['D'] if pd.notna(df.iloc[i]['D']) else '应急措施'
        }

        # 生成段落
        paragraph = template.format(**row_data)
        paragraphs.append(paragraph)

    return paragraphs


# 任务2：生成BIO标注
def generate_bio_tags(paragraphs, df):
    """生成BIO标注"""
    # 实体类别定义
    entity_types = {
        'A': '危险源',
        'B': '潜在风险',
        'C': '事故类型',
        'D': '处置措施'
    }

    bio_results = []

    # 添加实体类别行
    bio_results.append("实体类别：危险源、潜在风险、事故类型、处置措施")

    for i, paragraph in enumerate(paragraphs):
        bio_tags = []
        chars = list(paragraph)

        # 获取当前行的实体内容
        row_idx = i + 1
        entities = {}
        # 对A、B、C、D列进行实体标注
        for col in ['A', 'B', 'C', 'D']:
            if col in df.columns and row_idx < len(df):
                content = str(df.iloc[row_idx][col])
                if pd.notna(df.iloc[row_idx][col]) and content != 'nan':
                    entities[content] = entity_types[col]

        # 标注BIO标签
        j = 0
        while j < len(chars):
            char = chars[j]
            tagged = False

            # 检查是否匹配任何实体（按长度降序排列，优先匹配长实体）
            sorted_entities = sorted(entities.items(), key=lambda x: len(x[0]), reverse=True)
            for entity, entity_type in sorted_entities:
                if paragraph[j:j + len(entity)] == entity:
                    # 首字标注B-标签，其余字符标注I-标签（包括标点符号）
                    bio_tags.append(f'B-{entity_type}')
                    for k in range(1, len(entity)):
                        bio_tags.append(f'I-{entity_type}')
                    j += len(entity)
                    tagged = True
                    break

            if not tagged:
                # 连接词、标点符号标注为O
                bio_tags.append('O')
                j += 1

        # 组合字符和标签
        bio_line = ' '.join([f'{char}/{tag}' for char, tag in zip(chars, bio_tags)])
        bio_results.append(bio_line)

    return bio_results


# 任务3：生成关系标签
def generate_relation_labels(paragraphs, df):
    """生成关系标签"""
    relations = []

    # 实体类别定义
    entity_types = {
        'A': '危险源',
        'B': '潜在风险',
        'C': '事故类型',
        'D': '处置措施'
    }

    for i, paragraph in enumerate(paragraphs):
        row_idx = i + 1
        if row_idx >= len(df):
            continue

        # 获取实体内容
        entities = {}
        for col in ['A','B', 'C', 'D']:
            if col in df.columns:
                content = str(df.iloc[row_idx][col])
                if pd.notna(df.iloc[row_idx][col]) and content != 'nan':
                    entities[col] = content

        # 构建新格式的关系数据
        relation_data = {
            'id': i,
            'text': paragraph,
            'entity_list': [],
            'relation_list': []
        }

        # 查找实体在文本中的位置并构建entity_list
        entity_id_map = {}  # 列名到实体ID的映射
        entity_counter = 1

        for col, content in entities.items():
            start_pos = paragraph.find(content)
            if start_pos != -1:
                entity_id = f"E{entity_counter}"
                entity_id_map[col] = entity_id

                entity_info = {
                    "id": entity_id,
                    "entity": content,
                    "type": entity_types[col],
                    "start": start_pos,
                    "end": start_pos + len(content)
                }
                relation_data['entity_list'].append(entity_info)
                entity_counter += 1

        # 3种关系类型
        relation_types = [
            ('A', 'B', '引发'),      # 危险源-引发-潜在风险
            ('B', 'C', '产生'),      # 潜在风险-产生-事故类型
            ('D', 'C', '应对')       # 处置措施-应对-事故类型
        ]

        # 构建relation_list
        for head_col, tail_col, rel_type in relation_types:
            if head_col in entity_id_map and tail_col in entity_id_map:
                relation_info = {
                    "type": rel_type,
                    "head": {
                        "id": entity_id_map[head_col],
                        "entity": entities[head_col]
                    },
                    "tail": {
                        "id": entity_id_map[tail_col],
                        "entity": entities[tail_col]
                    }
                }
                relation_data['relation_list'].append(relation_info)

        relations.append(relation_data)

    return relations


# 主函数
def main():
    # 读取数据（请输入您的Excel文件路径）
    file_path = input("请输入Excel文件路径（直接回车使用示例数据）: ").strip()
    if not file_path:
        file_path = '应急.xlsx'

    print("正在读取数据...")
    df = read_excel_data(file_path)

    # 显示列信息
    print(f"数据shape: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print("前几行数据:")
    print(df.head())

    # 任务1：生成段落
    print("\n正在生成段落...")
    paragraphs = generate_paragraphs(df)

    with open('02text.txt', 'w', encoding='utf-8') as f:
        for para in paragraphs:
            f.write(para + '\n')
    print(f"已生成 {len(paragraphs)} 个段落，保存到 02text.txt")

    # 任务2：生成BIO标注
    print("正在生成BIO标注...")
    bio_tags = generate_bio_tags(paragraphs, df)

    with open('02BIO.txt', 'w', encoding='utf-8') as f:
        for bio_line in bio_tags:
            f.write(bio_line + '\n')
    print(f"已生成BIO标注，保存到 02BIO.txt")

    # 任务3：生成关系标签
    print("正在生成关系标签...")
    relations = generate_relation_labels(paragraphs, df)

    with open('02RE.json', 'w', encoding='utf-8') as f:
        for relation in relations:
            f.write(json.dumps(relation, ensure_ascii=False) + '\n')
    print(f"已生成关系标签，保存到 02RE.json")

    print("所有任务完成！")

    # 显示示例结果
    if paragraphs:
        print("\n=== 示例结果 ===")
        print(f"段落示例: {paragraphs[0]}")
        if len(bio_tags) > 1:
            print(f"BIO标注示例: {bio_tags[1][:150]}...")
        if relations:
            print(f"关系标签示例: {json.dumps(relations[0], ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()