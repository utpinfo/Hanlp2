import hanlp
import torch

"""
Service層
"""
 # 設定線程數 (MAC: sysctl -n hw.physicalcpu, Debian: grep -c ^processor /proc/cpuinfo)
torch.set_num_threads(8)  # 物理核心數
torch.set_num_interop_threads(8)
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')

# 加载用户自定义词典
custom_dict = {}
with open("./data/dict/dict1.txt", "r", encoding="utf-8") as f:
    for line in f:
        word, tag = line.strip().split()
        custom_dict[word] = tag  # 例如: 借样 NN
tokenizer.dict_force = custom_dict

pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
ner_model = hanlp.load('./data/model/ner/product_bert')

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

    # 覆盖 POS：如果 token 在自定义词典里，就强制用词典里的 POS
    for i, tok in enumerate(tokens):
        if tok in custom_dict:
            pos_tags[i] = custom_dict[tok]

    # 將實體(NER) span 轉成逐 token NER
    for entity_text, entity_type, start, end in res['ner']:
        for i in range(start, end):
            ner_tags[i] = entity_type

    # JSON 輸出
    output = [
        {"token": t, "pos": p, "ner": n}
        for t, p, n in zip(tokens, pos_tags, ner_tags)
    ]
    return output
