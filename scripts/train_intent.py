import glob
import torch
import os
from hanlp.components.classifiers.transformer_classifier_tf import TransformerClassifierTF

"""
* 初始化訓練 Intent
* 格式：TSV/CSV (text \t label)
* 加速 (INTEL)
pip install --upgrade intel-tensorflow
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
ncpu = os.cpu_count()
if ncpu > 0:
    torch.set_num_threads(ncpu)
    torch.set_num_interop_threads(ncpu)

# 定義訓練檔案和合併檔案路徑
train_dir = '../data/train/intent'
train_files = glob.glob(os.path.join(train_dir, 'source_*.tsv'))
train_file = os.path.join(train_dir, 'train.tsv')
save_dir = '../data/model/intent/bert_base'

# 自動合併檔案
with open(train_file, 'w', encoding='utf-8') as outfile:
    for file in train_files:
        with open(file, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
            outfile.write('\n')

# 訓練 Intent 模型
classifier =  TransformerClassifierTF()
classifier.fit(
    #trn_data=CHNSENTICORP_ERNIE_TRAIN,  # 訓練數據 (TSV: text \t label)
    #dev_data=CHNSENTICORP_ERNIE_DEV,  # 驗證數據
    trn_data=train_file,  # 訓練數據 (TSV: text \t label)
    dev_data=os.path.join(train_dir, 'dev.tsv'),  # 驗證數據
    save_dir=save_dir,  # 模型輸出目錄
    transformer='bert-base-chinese',  # 預訓練模型
    epochs=5,  # 訓練輪數 (小數據集建議 20~50，大數據 5~10 就夠)
    batch_size=8,  # batch size
)

"""
# 測試
classifier = hanlp.load(save_dir)
test_sentences = ['查询DY01库存', '我想退貨', '開會時間是什麼時候']
results = classifier.predict(test_sentences)
print(results)  # ['查庫存', '退貨', '問時間']
"""

# 評估
classifier.evaluate(os.path.join(train_dir, 'dev.tsv'), save_dir)
