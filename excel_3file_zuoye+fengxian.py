import pandas as pd
import random
import json
import re


# 读取Excel文件数据
def read_excel_data(file_path):
    """读取Excel文件数据"""
    try:
        df = pd.read_excel(file_path)
        # 重命名列为A, B, C, D, E, F, G, H便于处理
        if len(df.columns) >= 8:
            df.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] + list(df.columns[8:])
        return df
    except Exception as e:
        print(f"读取Excel文件出错: {e}")
        print("使用示例数据...")
        # 如果没有文件，使用示例数据
        data = {
            'A': ['施工位置'] + ['通用作业'] * 18,
            'B': ['施工活动'] + ['支架工程'] * 8 + ['模板工程'] * 10,
            'C': ['作业要求'] + ['支架拆除施工'] * 8 + ['模板安装施工'] * 10,
            'D': ['作业要求内容...'] * 19,
            'E': ['危险源'] + ['通用作业'] * 18,
            'F': ['潜在风险'] + ['支架搭拆作业'] * 8 + ['模板搭拆作业'] * 10,
            'G': ['预防措施'] + ['坍塌倾覆风险'] * 8 + ['高处坠落风险'] * 10,
            'H': ['预防措施内容...'] * 19
        }
        return pd.DataFrame(data)


# 生成多样化的句式模板
def get_sentence_templates():
    """返回10种不同的句式模板"""
    templates = [
        "对于{A}，在{B}的{C}需遵循{D}。同时，对于该{E}的{F}，存在{G}，因此需实施{H}。",
        "在{A}中，{B}作业时{C}应当{D}。针对可能出现的{E}带来的{F}，需要采取{G}措施，具体包括{H}。",
        "关于{A}的{B}，其{C}必须符合{D}的要求。由于{E}可能导致{F}的发生，故应执行{G}，特别是{H}。",
        "针对{A}范围内的{B}，{C}过程中应严格按照{D}执行。考虑到{E}存在{F}的隐患，必须落实{G}，重点关注{H}。",
        "在{A}施工中，{B}的{C}需要遵循{D}标准。鉴于{E}会引起{F}，应当建立{G}机制，确保{H}得到有效实施。",
        "对于{A}作业区域，{B}实施时{C}应当依据{D}进行。为防范{E}造成的{F}，需建立{G}体系，包括{H}等措施。",
        "在{A}的施工过程中，{B}作业的{C}必须满足{D}。由于{E}潜在的{F}威胁，应制定{G}方案，明确{H}的具体要求。",
        "关于{A}工程，{B}施工中{C}需要严格执行{D}。考虑{E}可能带来{F}，须采用{G}策略，特别强调{H}的重要性。",
        "针对{A}项目的{B}，{C}环节应当遵照{D}实施。面对{E}引发的{F}挑战，应部署{G}措施，尤其要落实{H}。",
        "在{A}工作中，{B}的{C}操作需按{D}规范执行。为应对{E}产生的{F}，必须启动{G}程序，重点实施{H}。"
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
            'A': df.iloc[i]['A'] if pd.notna(df.iloc[i]['A']) else '作业区域',
            'B': df.iloc[i]['B'] if pd.notna(df.iloc[i]['B']) else '施工活动',
            'C': df.iloc[i]['C'] if pd.notna(df.iloc[i]['C']) else '作业内容',
            'D': df.iloc[i]['D'] if pd.notna(df.iloc[i]['D']) else '相关要求',
            'E': df.iloc[i]['E'] if pd.notna(df.iloc[i]['E']) else '作业类型',
            'F': df.iloc[i]['F'] if pd.notna(df.iloc[i]['F']) else '风险类型',
            'G': df.iloc[i]['G'] if pd.notna(df.iloc[i]['G']) else '防控措施',
            'H': df.iloc[i]['H'] if pd.notna(df.iloc[i]['H']) else '具体措施'
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
        'B': '施工位置',
        'C': '施工活动',
        'D': '作业要求',
        'F': '危险源',
        'G': '潜在风险',
        'H': '预防措施'
    }

    bio_results = []

    # 添加实体类别行
    bio_results.append("实体类别：施工位置、施工活动、作业要求、危险源、潜在风险、预防措施")

    for i, paragraph in enumerate(paragraphs):
        bio_tags = []
        chars = list(paragraph)

        # 获取当前行的实体内容
        row_idx = i + 1
        entities = {}
        # 只对B、C、D、F、G、H列进行实体标注，A、E列标注为O
        for col in ['B', 'C', 'D', 'F', 'G', 'H']:
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
                # A列、E列内容和连接词、标点符号标注为O
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
        'B': '施工位置',
        'C': '施工活动',
        'D': '作业要求',
        'F': '危险源',
        'G': '潜在风险',
        'H': '预防措施'
    }

    for i, paragraph in enumerate(paragraphs):
        row_idx = i + 1
        if row_idx >= len(df):
            continue

        # 获取实体内容
        entities = {}
        for col in ['B', 'C', 'D', 'F', 'G', 'H']:
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

        # 6种关系类型
        relation_types = [
            ('C', 'B', '定位'),  # 施工活动-定位-施工位置
            ('C', 'D', '遵循'),  # 施工活动-遵循-作业要求
            ('C', 'F', '发现'),  # 施工活动-发现-危险源
            ('F', 'G', '引发'),  # 危险源-引发-潜在风险
            ('D', 'H', '实施'),  # 作业要求-实施-预防措施
            ('H', 'G', '预防')  # 预防措施-预防-潜在风险
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
        file_path = '作业+风险.xlsx'

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

    with open('01text.txt', 'w', encoding='utf-8') as f:
        for para in paragraphs:
            f.write(para + '\n')
    print(f"已生成 {len(paragraphs)} 个段落，保存到 01text.txt")

    # 任务2：生成BIO标注
    print("正在生成BIO标注...")
    bio_tags = generate_bio_tags(paragraphs, df)

    with open('01BIO.txt', 'w', encoding='utf-8') as f:
        for bio_line in bio_tags:
            f.write(bio_line + '\n')
    print(f"已生成BIO标注，保存到 01BIO.txt")

    # 任务3：生成关系标签
    print("正在生成关系标签...")
    relations = generate_relation_labels(paragraphs, df)

    with open('01RE.json', 'w', encoding='utf-8') as f:
        for relation in relations:
            f.write(json.dumps(relation, ensure_ascii=False) + '\n')
    print(f"已生成关系标签，保存到 01RE.json")

    print("所有任务完成！")

    # 显示示例结果
    if paragraphs:
        print("\n=== 示例结果 ===")
        print(f"段落示例: {paragraphs[0][:100]}...")
        if len(bio_tags) > 1:
            print(f"BIO标注示例: {bio_tags[1][:100]}...")
        if relations:
            print(f"关系标签示例: {json.dumps(relations[0], ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()
