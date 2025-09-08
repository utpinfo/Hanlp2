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

# 3️⃣ 處理函數
def process_text_to_json(text):
    """
    輸入中文文本，輸出 JSON 格式，每個 token 包含分詞、詞性、NER
    """
    res = pipeline(text)
    tokens = res['tok']
    pos_tags = res['pos']
    ner_tags = ['O'] * len(tokens)

    # 將實體 span 轉成逐 token NER
    for entity_text, entity_type, start, end in res['ner']:
        for i in range(start, end):
            ner_tags[i] = entity_type

    # 生成 JSON 結構
    output = [
        {"token": t, "pos": p, "ner": n}
        for t, p, n in zip(tokens, pos_tags, ner_tags)
    ]
    return json.dumps(output, ensure_ascii=False, indent=2)

# 4️⃣ 測試
if __name__ == "__main__":
    sentence = "查询71001对账单"
    json_result = process_text_to_json(sentence)
    print(json_result)
