import json


def jsonl_to_json(jsonl_file, json_file):
    """
    将JSONL文件转换为JSON文件

    参数:
    jsonl_file (str): JSONL文件的路径
    json_file (str): 要保存的JSON文件的路径
    """
    # 读取JSONL文件中的所有行
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        # 每行解析为一个JSON对象，并收集到一个列表中
        json_list = [json.loads(line) for line in f if line.strip()]

    # 将列表写入JSON文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_list, f, ensure_ascii=False, indent=4)

    print(f"转换完成！已将{jsonl_file}转换为{json_file}")


# 使用示例
jsonl_file_path = 'D:\Carina-cxp\CSU\知识图谱\数据预处理\风险提示卡_全部单位工程_全部实体_中文标签.jsonl'  # 修改为你的JSONL文件路径
json_file_path = 'D:\Carina-cxp\CSU\知识图谱\数据预处理\风险提示卡_全部单位工程_全部实体_中文标签.json'  # 修改为要保存的JSON文件路径

jsonl_to_json(jsonl_file_path, json_file_path)