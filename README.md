# 環境配置
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

# 目錄結構
- mkdir data
- touch data/trian.txt (80%數據)
- touch data/dev.txt (20%數據)
-->  

# 準備材料
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

# 训练HANLP2
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
    transformer='bert-base-chinese',# bert-base-chinese 或 electra-small (CPU慢), 可選: 1.FINE_ELECTRA_SMALL_ZH MSRA_NER_ELECTRA_SMALL_ZH
    epochs=10,
    batch_size=8,
    word_dropout=0.05,
    delimiter_in_entity='-',
    char_level=True   # 👈 加這個
)

recognizer = hanlp.load(save_dir)
test_sentences = '查询博士伦-XY99库存'
results = recognizer.predict(test_sentences)
print(results)
```


# 测试
```
import hanlp

# 載入你訓練好的模型
ner = hanlp.load('product_ner_model')

text = "查询海俪恩-120013-L000P3 偏光库存"
result = ner(text)

print(result)
```

# 測試[2]
```python
# 1️⃣ 加载模型
import hanlp

# 1️⃣ 加载模型
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')  # 分詞器
pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB5_POS_RNN)  # 詞性標註器
ner_model = hanlp.load('data/model/ner/product_bert')  # 命名實體識別模型

# 2️⃣ 构建 pipeline
pipeline = hanlp.pipeline() \
    .append(tokenizer, output_key='tok') \
    .append(pos_tagger, input_key='tok', output_key='pos') \
    .append(ner_model, input_key='tok', output_key='ner')

# 3️⃣ 测试句子
sentence = '查询ME&CITY4支装展架（太阳镜）库存'
res = pipeline(sentence)

# 4️⃣ 输出每个词的分词、词性、NER
for token, pos, ner in zip(res['tok'], res['pos'], res['ner']):
    print(token, pos, ner)

```

# 啟動API
```shell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

# 開機自動啟動
```shell
sudo systemctl daemon-reload
sudo systemctl enable hanlp_api.service  # 開機自動啟動
sudo systemctl start hanlp_api.service   # 立即啟動
```

# 自動文件
```shell
cat << EFO > /etc/systemd/system/hanlp_api.service
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

# 目錄結構
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


# 訓練重點
- B-NR 跟 E-NR 之間的I-NR內容格式需要多元

# 文件
- https://hanlp.hankcs.com/docs/api/hanlp/pretrained/ner.html
- https://hanlp.hankcs.com/demos/tok.html
