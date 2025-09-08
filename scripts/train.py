import glob

import hanlp
import os

"""
* 初始化訓練
# 加速 (INTEL)
pip install --upgrade intel-tensorflow
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 只顯示 Error
from hanlp.components.ner.transformer_ner import TransformerNamedEntityRecognizer

# 定義訓練檔案和合併檔案路徑
train_files = glob.glob('../data/train/source_*.txt')
merged_train_file = '../data/train/merged_train.txt'

# 自動合併檔案
with open(merged_train_file, 'w', encoding='utf-8') as outfile:
    for train_file in train_files:
        with open(train_file, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
            outfile.write('\n')  # 確保檔案間換行分隔

# 訓練模型
recognizer = TransformerNamedEntityRecognizer()
save_dir = '../data/model/ner/product_bert'

recognizer.fit(
    trn_data=merged_train_file,  # 使用合併後的檔案
    dev_data='../data/train/dev.txt',
    save_dir=save_dir,
    transformer='bert-base-chinese',
    # bert-base-chinese 或 electra-small (CPU慢), 可選: 1.FINE_ELECTRA_SMALL_ZH MSRA_NER_ELECTRA_SMALL_ZH
    epochs=10,
    batch_size=8,
    word_dropout=0.05,
    delimiter_in_entity='-',
    char_level=True  # 👈 加這個
)

recognizer = hanlp.load(save_dir)
test_sentences = '查询博士伦-XY99库存'
results = recognizer.predict(test_sentences)
print(results)
