import hanlp

# 载入模型
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')
pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
ner_model = hanlp.load('../data/model/ner/product_bert')

# 建立 pipeline
pipeline = hanlp.pipeline() \
    .append(tokenizer, output_key='tok') \
    .append(pos_tagger, input_key='tok', output_key='pos') \
    .append(ner_model, input_key='tok', output_key='ner')


def debug_ner(text):
    res = pipeline(text)
    tokens = res['tok']
    print(f"Tokens: {tokens}")

    # 打印 NER 模型原始输出
    print("Raw NER output (entity_text, entity_type, start, end):")
    for entity_text, entity_type, start, end in res['ner']:
        # 映射到 token
        token_span = tokens[start:end] if isinstance(start, int) else "Check span type"
        print(f"Entity: {entity_text}, Type: {entity_type}, Char/Token span: ({start}, {end}), Tokens: {token_span}")

    # 可选：每个 token 对应的 NER 标签
    ner_tags = ['O'] * len(tokens)
    for entity_text, entity_type, start, end in res['ner']:
        for i in range(start, end):
            ner_tags[i] = entity_type
    print("Token-level NER:")
    for t, n in zip(tokens, ner_tags):
        print(f"{t}: {n}")


if __name__ == "__main__":
    sentence = "查询冯凯HN0对账单"
    debug_ner(sentence)
