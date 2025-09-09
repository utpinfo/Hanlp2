import hanlp
import json

# 1️⃣ 載入模型
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')  # 分詞器
pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)  # 詞性標註器
ner_model = hanlp.load('../data/model/ner/product_bert')  # 自訓練的 NER 模型

# 2️⃣ 建立 pipeline

pipeline = hanlp.pipeline() \
    .append(tokenizer, output_key='tok') \
    .append(pos_tagger, input_key='tok', output_key='pos') \
    .append(ner_model, input_key='tok', output_key='ner')

# 4️⃣ 測試
if __name__ == "__main__":
    sentence = "查询江苏冯凯对账单"
    result = pipeline(sentence)
    print(result['tok'])
    print(result['ner'])