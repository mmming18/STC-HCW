# STC-HCW
**A Safety Training Corpus for Highway Construction Workers**

Python scripts and utilities for creating STC-HCW, a comprehensive corpus designed for natural language processing tasks in highway construction safety training.

## 📋 Overview

This repository contains utility scripts and datasets for natural language processing tasks, mainly for entity recognition (NER) and relation extraction (RE) tasks.

## 📁 Repository Structure

```
STC-HCW/
├── README.md
├── README_EN.md
├── scripts/           # All python scripts 
│   ├── ner_tasks/     # NER task related scripts
│   │   ├── jsonl_to_json.py
│   │   ├── json_to_bio.py
│   │   ├── csv_to_bio_fengxian.py
│   │   ├── csv_to_bio_yingji.py
│   │   ├── csv_to_bio_zuoye.py
│   │   ├── csv_to_txt_fengxian.py
│   │   ├── csv_to_txt_yingji.py
│   │   └── csv_to_txt_zuoye.py
│   ├── triple_extraction/  # Triplet extraction related scripts
│   │   ├── excel_3file_yingji.py
│   │   └── excel_3file_zuoye+fengxian.py
│   └── utils/         # General data processing scripts
│       ├── BIO_check.py
│       ├── bio_delete.py
│       ├── bio_merge.py
│       ├── bio_spilt.py
│       └── xlsx_to_csv.py
├── data/              # NER task related data
└── data02/            # Triplet extraction related data
```

## 🛠️ Script Categories

### 🔹 Group 1 (01data_preprocess): NER Tasks (Doccano Integration)
**Scripts:** `jsonl_to_json.py` | `json_to_bio.py`

**Purpose:** Process annotation data from Doccano platform
- Convert JSONL format to JSON format
- Transform JSON annotations to BIO-tagged text files
- Generate training data directly for NER model training

**Workflow:**
```
Doccano Platform → JSONL → JSON → BIO-tagged TXT
```

---

### 🔹 Group 2 (02data_preprocess): NER Tasks (Keyword System)
**Scripts:**
- **Text Generation:** `csv_to_txt_fengxian.py` | `csv_to_txt_yingji.py` | `csv_to_txt_zuoye.py`
- **BIO Annotation:** `csv_to_bio_fengxian.py` | `csv_to_bio_yingji.py` | `csv_to_bio_zuoye.py`

**Purpose:** Generate training data from keyword taxonomy tables
- Convert classified keyword tables (CSV) to documents (TXT) using sentence templates
- Generate BIO-tagged files directly from keyword tables
- Support three domains: 风险 (Risk), 应急 (Emergency), 作业 (Operation)

**Workflow:**
```
CSV Keyword Tables → Sentence Templates → BIO-tagged Files
```

---

### 🔹 Group 3 (03data_preprocess): Triple Extraction (NER + RE Tasks)
**Scripts:** `excel_3file_zuoye+fengxian.py` | `excel_3file_yingji.py`

**Purpose:** Generate comprehensive training data for both NER and RE tasks
- **Output 1:** `text.txt` - Generated paragraphs from keywords
- **Output 2:** `BIO.txt` - BIO-tagged annotation file
- **Output 3:** `RE.json` - Relation extraction annotation file

**Workflow:**
```
CSV Keyword Tables → 3 Files (Text + BIO + RE)
```

---

### 🔹 Group 4 (04data_preprocess): General Data Processing
**Scripts:** `BIO_check.py` | `bio_delete.py` | `bio_merge.py` | `bio_spilt.py` | `xlsx_to_csv.py`

| Script | Function |
|--------|----------|
| `BIO_check.py` | Check BIO format errors and generate corrected files |
| `bio_delete.py` | Remove lines with specific labels from BIO files |
| `bio_merge.py` | Merge multiple BIO files into one |
| `bio_spilt.py` | Split single BIO file into multiple equal parts |
| `xlsx_to_csv.py` | Convert XLSX to CSV format with error line removal |

## 📂 Data Directories

### `data/` Directory
Contains processed files from **Groups 1 & 2** scripts, ready for NER task training.

### `data02/` Directory
Contains processed files from **Group 3** scripts, ready for triple extraction (NER + RE) task training.

## 🚀 Usage Recommendations

### Workflow Options:

1. **Using Doccano Platform:**
   ```
   Manual Annotation → Group 1 Scripts → NER Training Data
   ```

2. **Using Keyword System:**
   ```
   Keyword Tables → Group 2 Scripts → Auto-generated Annotation Data
   ```

3. **Triple Extraction Tasks:**
   ```
   Keyword Tables → Group 3 Scripts → NER + RE Training Data
   ```

4. **Data Processing:**
   ```
   Raw Data → Group 4 Scripts → Format Check/Split/Merge Operations
   ```

## 🎯 Domain Categories

| Category | English | Description |
|----------|---------|-------------|
| **fengxian** | Risk | Risk/Hazard identification |
| **yingji** | Emergency | Emergency response |
| **zuoye** | Work | Work operations |

## 🔧 Getting Started

1. Choose your data source (Doccano annotations or keyword tables)
2. Select appropriate script group based on your task
3. Run the corresponding scripts to generate training data
4. Use Group 4 scripts for additional data processing if needed
