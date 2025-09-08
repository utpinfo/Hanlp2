import glob

from hanlp.components.ner.transformer_ner import TransformerNamedEntityRecognizer
import os
"""
* 增量訓練
"""
# 定義訓練檔案和合併檔案路徑
train_files = glob.glob('../data/train/source_*.txt')
merged_train_file = '../data/train/merged_train.txt'

# 自動合併檔案
with open(merged_train_file, 'w', encoding='utf-8') as outfile:
    for train_file in train_files:
        with open(train_file, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
            outfile.write('\n')  # 確保檔案間換行分隔

# 載入已訓練的模型
recognizer = TransformerNamedEntityRecognizer()
recognizer.load('../data/model/ner/product_bert')  # 原本模型權重

# 用合併後的檔案微調
recognizer.fit(
    trn_data=merged_train_file,  # 使用合併後的檔案
    dev_data='../data/train/dev.txt',
    save_dir='../data/model/ner/product_bert_finetuned',  # 保存新模型
    transformer='bert-base-chinese',
    epochs=3,  # 微調輪數
    batch_size=8,
    word_dropout=0.05,
    delimiter_in_entity='-',
    char_level=True
)
