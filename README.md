# STC-HCW
**高速公路施工建筑工人安全培训语料库**

## 📋 项目概述

本仓库包含用于自然语言处理任务的实用工具脚本及数据集，主要用于实体识别（NER）和关系抽取（RE）任务。

## 📁 仓库结构

```
STC-HCW/
├── README.md                   # 中文版README文件
├── README_EN.md                # English version of the README file
├── 01data_preprocess/          # doccano 平台相关数据预处理脚本
│   ├── jsonl_to_json.py
│   └── json_to_bio.py
├── 02data_preprocess/           # NER任务相关数据预处理脚本
│   ├── csv_to_bio_fengxian.py
│   ├── csv_to_bio_yingji.py
│   ├── csv_to_bio_zuoye.py
│   ├── csv_to_txt_fengxian.py
│   ├── csv_to_txt_yingji.py
│   └── csv_to_txt_zuoye.py
├── 03data_preprocess/           # 三元组抽取任务相关数据预处理脚本
│   ├── excel_3file_yingji.py
│   └── excel_3file_zuoye+fengxian.py
├── 04data_preprocess/           # 通用数据处理脚本
│   ├── BIO_check.py
│   ├── bio_delete.py
│   ├── bio_merge.py
│   ├── bio_spilt.py
│   └── xlsx_to_csv.py
├── data/                       # 可用于NER任务的数据集
└── 02data/                     # 可用于三元组抽取任务（NER+RE）的数据集
```

## 🛠️ 脚本功能分类

### 🔹 第一组01data_preprocess：NER 任务（Doccano 平台集成）
**脚本路径：** `01data_preprocess/jsonl_to_json.py` | `01data_preprocess/json_to_bio.py`

**用途：** 处理来自 Doccano 标注平台的数据
- 将需要标注的文本上传到 Doccano 平台
- 导出标注数据时，部分设备只能导出 JSONL 格式
- `jsonl_to_json.py` 将 JSONL 格式转换为 JSON 格式
- `json_to_bio.py` 将带有标注内容的 JSON 文件转换为 BIO 标注的 TXT 文件

**处理流程：**
```
Doccano 平台 → JSONL 格式 → JSON 格式 → BIO 标注文件
```

---

### 🔹 第二组02data_preprocess：NER 任务（关键词体系）
**脚本路径：**
- **文本生成：** `02data_preprocess/csv_to_txt_fengxian.py` | `02data_preprocess/csv_to_txt_yingji.py` | `02data_preprocess/csv_to_txt_zuoye.py`
- **BIO 标注：** `02data_preprocess/csv_to_bio_fengxian.py` | `02data_preprocess/csv_to_bio_yingji.py` | `02data_preprocess/csv_to_bio_zuoye.py`

**用途：** 从关键词体系表格自动生成训练数据
- `csv_to_txt` 系列：将分类好的关键词体系表格（CSV 格式）依据设定好的句式模板生成文档（TXT 格式）
- `csv_to_bio` 系列：在句式模板生成句子的基础上，将表格内的关键词标注 B/I/O 实体标签，直接生成 BIO 标注文件

**处理流程：**
```
CSV 关键词表格 → 句式模板 → BIO 标注文件
```

---

### 🔹 第三组03data_preprocess：三元组抽取（NER + RE 任务）
**脚本路径：** `03data_preprocess/excel_3file_zuoye+fengxian.py` | `03data_preprocess/excel_3file_yingji.py`

**用途：** 同时生成 NER 和 RE 任务的训练数据
- **输出1：** `text.txt` - 将表格内关键词依据句式模板生成的段落
- **输出2：** `BIO.txt` - 在段落基础上标注 B/I/O 实体标签的 BIO 标注文件
- **输出3：** `RE.json` - 将关键词依据关系规则模板组成三元组的关系标注文件

**处理流程：**
```
CSV 关键词表格 → 三个文件（文本 + BIO 标注 + 关系标注）
```

---

### 🔹 第四组04data_preprocess：通用数据处理
**脚本路径：** `04data_preprocess/BIO_check.py` | `04data_preprocess/bio_delete.py` | `04data_preprocess/bio_merge.py` | `04data_preprocess/bio_spilt.py` | `04data_preprocess/xlsx_to_csv.py`

| 脚本 | 功能说明 |
|------|----------|
| `04data_preprocess/BIO_check.py` | 检查 BIO 标注文件是否存在格式错误，删除错误行生成正确格式的文件 |
| `04data_preprocess/bio_delete.py` | 删除 BIO 标注文件中具备特定标签的行 |
| `04data_preprocess/bio_merge.py` | 将多个 BIO 标注文件合并为一个 |
| `04data_preprocess/bio_spilt.py` | 将单个 BIO 标注文件拆分为均等的多个文件 |
| `04data_preprocess/xlsx_to_csv.py` | 将 XLSX 格式文件转为 CSV 格式，并按要求删除错误行 |

## 📂 数据文件夹说明

### `data/` 文件夹
存储了利用第一组、第二组python代码进行数据处理工作的过程文件，内部文件可直接用于NER任务。

### `02data/` 文件夹
存储了利用第三组python代码进行数据处理工作的过程文件，内部文件可直接用于三元组抽取（NER+RE）任务。

## 🔒 访问限制说明
- 由于数据文件的敏感性和大小考虑，上述两个数据文件夹已设置为指向私有仓库的 Git 子模块。
- 目录结构可见：您可以在本仓库中查看完整的文件夹结构和文件列表
- 内容访问受限：实际文件内容存储在私有仓库中，需要特定权限才能访问
- 申请访问权限：如需访问完整数据文件，请联系仓库维护者申请相应私有仓库的访问权限

### `data_preprocess/` 文件夹组
- **`01data_preprocess/`**：Doccano 平台数据处理脚本
- **`02data_preprocess/`**：NER任务数据处理脚本
- **`03data_preprocess/`**：三元组抽取任务数据处理脚本
- **`04data_preprocess/`**：通用数据处理工具脚本

## 📊 生成数据说明

- **BIO 标注文件**：可直接用于 NER 任务的模型训练
- **RE 关系文件**：可直接用于关系抽取任务的模型训练
- **文本文件**：包含文本段落

## 🚀 使用建议

### 工作流程选择：

1. **使用 Doccano 标注平台：**
   ```
   人工标注 → 第一组脚本 → 获得 NER 训练数据
   ```

2. **使用关键词体系表格：**
   ```
   关键词表格 → 第二组脚本 → 自动生成标注数据
   ```

3. **需要三元组数据：**
   ```
   关键词表格 → 第三组脚本 → 同步生成实体和关系标注
   ```

4. **数据处理过程：**
   ```
   原始数据 → 第四组脚本 → 格式检查/拆分/合并等操作
   ```

## 🎯 领域分类

| 分类代码 | 中文名称 | 说明 |
|----------|----------|------|
| **fengxian** | 风险防控 | 风险识别与安全隐患 |
| **yingji** | 应急处置 | 应急响应与处置 |
| **zuoye** | 作业控制 | 作业操作与规范 |

## 🔧 快速开始

1. **选择数据源**：确定使用 Doccano 标注数据还是关键词体系表格
2. **选择脚本组**：根据任务需求选择对应的脚本组
3. **运行脚本**：执行相应脚本生成训练数据
4. **数据处理**：根据需要使用第四组脚本进行额外的数据处理



