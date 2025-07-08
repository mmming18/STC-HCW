# STC-HCW
Python scripts and texts for creating STC‑HCW—A Safety Training Corpus for Highway Construction Workers.

本仓库包含用于自然语言处理任务的实用工具脚本，主要用于实体识别（NER）和关系抽取（RE）任务的数据处理与格式转换。


####文件列表
STC-HCW/
├── README.md
├── BIO_check.py
├── bio_delete.py
├── bio_merge.py
├── bio_spilt.py
├── csv_to_bio_fengxian.py
├── csv_to_bio_yingji.py
├── csv_to_bio_zuoye.py
├── csv_to_txt_fengxian.py
├── csv_to_txt_yingji.py
├── csv_to_txt_zuoye.py
├── excel_3file_yingji.py
├── excel_3file_zuoye+fengxian.py
├── json_to_bio.py
├── jsonl_to_json.py
├── xlsx_to_csv.py
├── data/            # NER任务数据
└── data02/          # 三元组抽取任务数据


####python脚本功能分类
##第一组：适用NER任务
jsonl_to_json.py\json_to_bio.py
用途：将需要标注的文本上传doccano平台，在导出标注好的数据时，部分设备只能导出为.jsonl格式。jsonl_to_json.py可将.jsonl格式文件转换为.json格式。json_to_bio.py
可将带有标注内容的.json格式文件转换为BIO标注的.txt文件。生成的BIO标注文件可直接用于NER任务的模型训练。
##第二组：适用NER任务
csv_to_bio_fengxian.py\csv_to_bio_yingji.py\csv_to_bio_zuoye.py
csv_to_txt_fengxian.py\csv_to_txt_yingji.py\csv_to_txt_zuoye.py
用途：csv_to_txt系列文件可将分类好的关键词体系表格（.csv格式）依据设定好的句式模板生成文档（.txt格式）。csv_to_bio系列文件可在按句式模板生成句子的基础上，将表格内的关键词标注B/I/O实体标签，直接由关键词体系表格（.csv格式）生成BIO标注文件（.txt格式）。生成的BIO标注文件可直接用于NER任务的模型训练。
##第三组：适用三元组抽取（NER+RE）任务
excel_3_file_zuoye+fengxian.py\excel_3_file_yingji.py
用途：输入关键词体系表格（.csv格式），输出三份文件。第一份输出为text.txt文件，可将表格内关键词依据句式模板生成段落。第二份输出为BIO.txt，在段落基础上，将表格内的关键词标注B/I/O实体标签，生成BIO标注文件。第三份输出为RE.json文件，在段落基础上，可将表格内关键词依据关系规则模板组成三元组，生成关系标签标注文件。生成的BIO.txt标注文件可用于NER任务的模型训练，而RE.json文件可用于RE任务的模型训练。
##第四组：通用数据处理BIO_check.py\bio_delete.py\bio_merge.py\bio_spilt.py\xlsx_to_csv.py
BIO_check.py用于检查BIO标注文件是否存在格式错误，并删除错误行生成正确格式的BIO标注文件
bio_delete.py用于删除BIO标注文件中具备特定标签的行。
bio_merge.py将多个BIO标注文件合并为一个。
bio_spilt.py将单个BIO标注文件拆分为均等的多个。
xlsx_to_csv.py将.xlsx格式文件转为.csv格式，并按要求删除错误行。


####数据文件夹说明
##data文件夹
包含使用第一组和第二组脚本处理后的文件，可直接用于NER任务训练。
##data02文件夹
包含使用第三组脚本处理后的文件，可直接用于三元组抽取（NER+RE）任务训练。


####使用建议
使用doccano标注数据 → 第一组脚本 → 获得NER训练数据
有关键词体系表格 → 第二组脚本 → 自动生成标注数据
需要三元组数据 → 第三组脚本 → 同步生成实体和关系标注
数据处理过程 → 第四组脚本 → 格式检查/拆分/合并等操作
