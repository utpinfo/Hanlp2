import hanlp
"""
Service層
"""
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')
pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
ner_model = hanlp.load('data/model/ner/product_bert')

# 建立 pipeline
pipeline = hanlp.pipeline() \
    .append(tokenizer, output_key='tok') \
    .append(pos_tagger, input_key='tok', output_key='pos') \
    .append(ner_model, input_key='tok', output_key='ner')

def ner_predict(text: str):
    res = pipeline(text)
    tokens = res['tok']
    pos_tags = res['pos']
    ner_tags = ['O'] * len(tokens)

    # 將實體 span 轉成逐 token NER
    for entity_text, entity_type, start, end in res['ner']:
        for i in range(start, end):
            ner_tags[i] = entity_type

    # JSON 輸出
    output = [
        {"token": t, "pos": p, "ner": n}
        for t, p, n in zip(tokens, pos_tags, ner_tags)
    ]
    return output
