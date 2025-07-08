import json
import os


def convert_doccano_to_bio(input_file, output_file):
    """
    将Doccano导出的JSON文件转换为BIO格式

    参数:
    input_file (str): Doccano JSON文件路径
    output_file (str): 输出的BIO格式文件路径
    """
    try:
        # 读取JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"成功读取文件: {input_file}")

        # 打开输出文件
        with open(output_file, 'w', encoding='utf-8') as out_f:
            # 如果是JSON数组，处理数组中的每个项目
            if isinstance(data, list):
                print(f"检测到JSON数组，共{len(data)}项")

                for i, item in enumerate(data):
                    process_item(item, out_f, i)
            else:
                # 如果是单个JSON对象
                print("检测到单个JSON对象")
                process_item(data, out_f, 0)

        print(f"处理完成，结果已保存至: {output_file}")
        return True

    except Exception as e:
        print(f"处理过程中出错: {e}")
        return False


def process_item(item, output_file, index):
    """处理单个JSON项目"""
    try:
        # 获取文本
        if 'text' not in item:
            print(f"项目 {index} 中未找到'text'字段，跳过")
            return

        text = item['text']
        print(f"处理项目 {index}，文本长度: {len(text)}")

        # 获取实体
        entities = []
        if 'entities' in item:
            entities = item['entities']

        # 初始化BIO标签
        bio_tags = ['O'] * len(text)

        # 填充BIO标签
        for entity in entities:
            # 根据实体数据结构提取信息
            if isinstance(entity, dict):
                # 检查是否包含id, label, start_offset, end_offset
                if 'label' in entity and 'start_offset' in entity and 'end_offset' in entity:
                    label = entity['label']
                    start = entity['start_offset']
                    end = entity['end_offset']
                else:
                    continue
            else:
                continue

            # 填充标签
            if 0 <= start < end <= len(text):
                bio_tags[start] = f'B-{label}'
                for i in range(start + 1, end):
                    bio_tags[i] = f'I-{label}'

        # 写入输出文件
        output_file.write(f"# 文本 {index + 1}\n")
        for char, tag in zip(text, bio_tags):
            output_file.write(f"{char}\t{tag}\n")
        output_file.write("\n")  # 文本间空行分隔

    except Exception as e:
        print(f"处理项目 {index} 时出错: {e}")


if __name__ == "__main__":
    # 设置文件路径
    input_file = r"D:\Carina-cxp\CSU\知识图谱\数据预处理\风险提示卡_全部实体.json"
    output_file = r"D:\Carina-cxp\CSU\知识图谱\数据预处理\风险提示卡_全部实体（1）_bio.txt"

    print("=" * 50)
    print("Doccano JSON 转 BIO 格式转换工具")
    print("=" * 50)

    if not os.path.exists(input_file):
        print(f"错误: 输入文件不存在: {input_file}")
        input("按回车键退出...")
        exit(1)

    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 执行转换
    success = convert_doccano_to_bio(input_file, output_file)

    if success:
        print("\n转换成功!")
        # 显示文件前几行
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                preview = f.read(500)
            print("\n输出文件预览:")
            print("-" * 50)
            print(preview)
            print("-" * 50)
        except Exception as e:
            print(f"无法预览输出文件: {e}")
    else:
        print("\n转换失败，请检查错误信息")

    input("\n按回车键退出...")