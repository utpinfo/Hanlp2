# 窮逼の自然語言模組

## 環境配置

- pyenv install 3.8.20
- pip install "hanlp[full]"
- pip install -r requirements.txt

<!--
# MAC M系列啟用GPU
pip install tensorflow-macos
pip install tensorflow-metal

import tensorflow as tf

print("TensorFlow 版本:", tf.__version__)
print("可用 GPU 数:", len(tf.config.list_physical_devices('GPU')))
print("设备列表:", tf.config.list_physical_devices())
-->

## 目錄結構生成

- mkdir data
- touch data/trian.txt (80%數據)
- touch data/dev.txt (20%數據)
  -->

## 工作流介紹 (HANLP2)

- TOKEN (分割句子成單位詞)

1. 在線模組: https://hanlp.hankcs.com/docs/api/hanlp/pretrained/tok.html
2. 專案模組: hanlp.pretrained.tok.FINE_ELECTRA_SMALL_ZH
3. 自定義字典

- POS (詞性)

1. 在線模組: https://hanlp.hankcs.com/docs/api/hanlp/pretrained/pos.html
2. 專案模組: hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL
3. 自定義命名規則

- NER (單位詞的命名)

1. 在線模組: https://hanlp.hankcs.com/docs/api/hanlp/pretrained/ner.html
2. 專案模組: transformer='bert-base-chinese'
3. 自定義命名規則

- SRL (語意角色)

1. 在線模組: https://hanlp.hankcs.com/docs/api/hanlp/pretrained/srl.html
2. 專案模組: hanlp.pretrained.srl.CPB3_SRL_ELECTRA_SMALL

## 準備材料 (BIO規範)

- 訓練資料 (data/train.txt)

```txt
我    O
想    O
查    O
博    B-PRODUCT
士    I-PRODUCT
伦    I-PRODUCT
-    I-PRODUCT
X    I-PRODUCT
Y    I-PRODUCT
9    I-PRODUCT
9    I-PRODUCT
库    O
存    O
```

- 驗證資料 (data/dev.txt)

```txt
查 O
询 O
紅 B-PRODUCT
蘋 I-PRODUCT
果 I-PRODUCT
库 O
存 O
```

## 训练HANLP2

```python
import hanlp
import os

"""
# 加速 (INTEL)
pip install --upgrade intel-tensorflow
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 只顯示 Error
from hanlp.components.ner.transformer_ner import TransformerNamedEntityRecognizer

recognizer = TransformerNamedEntityRecognizer()
save_dir = 'data/model/ner/product_bert'

recognizer.fit(
    trn_data='data/train.txt',
    dev_data='data/dev.txt',
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
```

## 测试

```
import hanlp

# 載入你訓練好的模型
ner = hanlp.load('product_ner_model')

text = "查询海俪恩-120013-L000P3 偏光库存"
result = ner(text)

print(result)
```

## 測試[2]

```python
# 1️⃣ 加载模型
import hanlp

# 1️⃣ 加载模型
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')  # 分詞器
pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB5_POS_RNN)  # 詞性標註器
ner_model = hanlp.load('data/model/ner/product_bert')  # 命名實體識別模型

# 2️⃣ 构建 pipeline
pipeline = hanlp.pipeline()
.append(tokenizer, output_key='tok')
.append(pos_tagger, input_key='tok', output_key='pos')
.append(ner_model, input_key='tok', output_key='ner')

# 3️⃣ 测试句子
sentence = '查询ME&CITY4支装展架（太阳镜）库存'
res = pipeline(sentence)

# 4️⃣ 输出每个词的分词、词性、NER
for token, pos, ner in zip(res['tok'], res['pos'], res['ner']):
    print(token, pos, ner)

```

## 啟動API

```shell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 開機自動啟動

```shell
sudo systemctl daemon-reload
sudo systemctl enable hanlp-api.service  # 開機自動啟動
sudo systemctl start hanlp-api.service   # 立即啟動
```

## 自動文件

```shell
cat << EFO > /etc/systemd/system/hanlp-api.service
[Unit]
Description=HanLP FastAPI Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/Hanlp2
Environment="PATH=/opt/Hanlp2/.venv/bin:/usr/bin:/bin"
ExecStart=/root/.pyenv/versions/3.8.20/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EFO
```

<!--
# 訪問路徑
http://127.0.0.1:8000/docs
-->

## 目錄結構

```text
Hanlp2/
├── app/                  # API 與程式碼
│   ├── __init__.py
│   ├── main.py           # FastAPI API
│   ├── pipeline.py       # NLP pipeline 封裝
│   └── utils.py          # 工具函數
├── data/                 # 訓練資料
│   ├── train.txt
│   ├── dev.txt
│   └── model/ner/product_bert/
├── scripts/              # 訓練、測試腳本
│   ├── train.py
│   └── test.py
├── tests/                # 單元測試
│   └── test_api.py
├── requirements.txt      # 套件依賴
└── README.md
```

## 訓練重點

- B-NR 跟 E-NR 之間的I-NR內容格式需要多元

## 文件

- https://hanlp.hankcs.com/docs/api/hanlp/pretrained/ner.html
- https://hanlp.hankcs.com/demos/tok.html
- https://hanlp.hankcs.com/docs/annotations/pos/ctb.html

## 最佳組合

- 代碼類 → tokenizer.dict_force (穩定、格式固定)
- 名稱類 → NER（DictionaryNER / 訓練模型）（不規則、變動多）

## 自定義辭典

BD = Business Document（缩写）

## 規則方案

- 推薦 (部分輸入詞: 馮凱, 可以匹配)

1. 字典加入全名： 楊馮凱
2. NER訓練集部分名：

```tsv
馮 B-AGENT
凱 I-AGENT
```

- 不推薦 (部分輸入詞: 馮凱, 無法匹配)

1. 字典加入全名： 楊馮凱
2. NER訓練集全名：

```tsv
楊 B-AGENT
馮 I-AGENT
凱 I-AGENT
```

# 訓練驗證
1. 訓練集loss仍下降 → 模型對訓練資料擬合能力還在提升
2. 驗證集 F1 已達滿分 → 模型在驗證集上已經沒有提升空間
3. 意味著, 再多跑幾個 epoch，驗證集性能不會提升, 繼續訓練可能導致過擬合
4. 過擬合（Overfitting）是指模型「記住訓練資料而不是學習規律」。
```
Epoch 1 / 10:
185/185 loss: 243.9575 P: 49.92% R: 73.29% F1: 59.39% ET: 19 m 31 s
185/185 loss: 0.1209 P: 99.99% R: 99.99% F1: 99.99% ET: 5 m 52 s
25 m 23 s / 4 h 13 m 50 s ETA: 3 h 48 m 27 s (saved)
Epoch 2 / 10:
185/185 loss: 4.0599 P: 69.94% R: 86.40% F1: 77.30% ET: 19 m 26 s
185/185 loss: 0.0554 P: 99.99% R: 99.99% F1: 99.99% ET: 5 m 46 s
50 m 47 s / 4 h 13 m 56 s ETA: 3 h 23 m 9 s (1)
Epoch 3 / 10:
185/185 loss: 1.8789 P: 78.52% R: 90.86% F1: 84.24% ET: 19 m 15 s
185/185 loss: 0.0540 P: 99.99% R: 99.99% F1: 99.99% ET: 5 m 46 s
1 h 15 m 48 s / 4 h 12 m 40 s ETA: 2 h 56 m 52 s (2)
Epoch 4 / 10:
185/185 loss: 1.0521 P: 83.28% R: 93.11% F1: 87.92% ET: 19 m 25 s
 58/185 loss: 0.0012 P: 100.00% R: 100.00% F1: 100.00% ETA: 4 m 18 s
```