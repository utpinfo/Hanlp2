import glob
import torch
import os
from hanlp.components.ner.transformer_ner import TransformerNamedEntityRecognizer

"""
* 初始化訓練 
# 格式 CoNLL/TSV
# 加速 (INTEL)
pip install --upgrade intel-tensorflow
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 只顯示 Error
# 設定線程數 (MAC: sysctl -n hw.physicalcpu, Debian: grep -c ^processor /proc/cpuinfo)
ncpu = os.cpu_count()
if ncpu > 0:
    torch.set_num_threads(ncpu)  # 根據 CPU 核心數調整
    torch.set_num_interop_threads(ncpu)  # 對跨操作符並行也使用

# 定義訓練檔案和合併檔案路徑
train_dir = '../data/train/ner'
train_files = glob.glob(os.path.join(train_dir, 'source_*.txt'))
train_file = os.path.join(train_dir, 'train.txt')
save_dir = '../data/model/ner/product_bert'

# 自動合併檔案
with open(train_file, 'w', encoding='utf-8') as outfile:
    for train_file in train_files:
        with open(train_file, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
            outfile.write('\n')  # 確保檔案間換行分隔

# 訓練模型
recognizer = TransformerNamedEntityRecognizer()
recognizer.fit(
    trn_data=train_file,  # 待訓練檔案 (材料)
    dev_data=os.path.join(train_dir, 'dev.txt'),  # 待驗證檔案 (材料)
    save_dir=save_dir,  # 結果
    transformer='bert-base-chinese',  # 底層語言模型 (字级模型)
    # bert-base-chinese 或 electra-small (CPU慢), 可選: 1.FINE_ELECTRA_SMALL_ZH MSRA_NER_ELECTRA_SMALL_ZH
    epochs=4,  # 訓練輪數 (整個訓練集「完整看一遍」算一次 epoch。調整10後正常)（<1k 條: 50, 1w ~ 10w 條:  10, >100w 條: 5）
    batch_size=32,  # 每次訓練的樣本數 （GPU 顯存充足：盡量設大一些，例如 32、64、128）
    # word_dropout=0.05, # 詞級別的隨機丟棄率
    delimiter_in_entity='',  # 實體內的詞分隔符
    char_level=True  # 👈 # 按字元級別處理 (char_level=True: 逐字[一行一字])
)
"""
recognizer = hanlp.load(save_dir)
test_sentences = '查询博士伦-XY99库存'
results = recognizer.predict(test_sentences)
print(results)
"""
recognizer.evaluate(os.path.join(train_dir, 'dev.txt'), save_dir)
