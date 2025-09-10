import hanlp
import json

# 1️⃣ 載入模型
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')  # 分詞器

# 2️⃣ 載入自定義詞典
custom_dict = {}
with open("../data/dict/dict1.txt", "r", encoding="utf-8") as f:
    for line in f:
        word, tag = line.strip().split()
        custom_dict[word] = tag  # 例如: 借樣 NN
tokenizer.dict_force = custom_dict

pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)  # 詞性標註器
ner_model = hanlp.load('../data/model/ner/product_bert')  # 自訓練的 NER 模型

# 3️⃣ 建立 pipeline
pipeline = hanlp.pipeline() \
    .append(tokenizer, output_key='tok') \
    .append(pos_tagger, input_key='tok', output_key='pos') \
    .append(ner_model, input_key='tok', output_key='ner')


# 4️⃣ 除錯函數
def debug_ner(text):
    """
    輸入文本，輸出分詞、詞性、NER，並優先使用自定義詞典的詞性
    """
    res = pipeline(text)
    tokens = res['tok']
    pos_tags = res['pos']
    ner_tags = ['O'] * len(tokens)

    # 後處理：優先使用自定義詞典的詞性
    for i, token in enumerate(tokens):
        if token in custom_dict:
            pos_tags[i] = custom_dict[token]  # 使用自定義詞典的詞性

    # 將實體 span 轉成逐 token NER
    for entity_text, entity_type, start, end in res['ner']:
        for i in range(start, end):
            ner_tags[i] = entity_type

    # 打印分詞結果
    print(f"Tokens: {tokens}")

    # 打印 NER 模型原始輸出
    print("Raw NER output (entity_text, entity_type, start, end):")
    for entity_text, entity_type, start, end in res['ner']:
        token_span = tokens[start:end] if isinstance(start, int) else "Check span type"
        print(f"Entity: {entity_text}, Type: {entity_type}, Char/Token span: ({start}, {end}), Tokens: {token_span}")

    # 打印每個 token 的信息
    print("Token-level NER and POS:")
    for t, n, p in zip(tokens, ner_tags, pos_tags):
        print(f"TOK: {t}: NER: {n} POS: {p}")


# 5️⃣ 測試
if __name__ == "__main__":
    sentence = "查询楊馮凱的借样"
    debug_ner(sentence)
