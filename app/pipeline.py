import hanlp
import torch
import os

"""
Service層
"""
# 設定線程數 (MAC: sysctl -n hw.physicalcpu, Debian: grep -c ^processor /proc/cpuinfo)
ncpu = os.cpu_count()
if ncpu > 0:
    torch.set_num_threads(ncpu)  # 根據 CPU 核心數調整
    torch.set_num_interop_threads(ncpu)  # 對跨操作符並行也使用
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')

cur_dir = os.path.dirname(os.path.abspath(__file__))  # 當前檔案所在目錄
prj_dir = os.path.dirname(cur_dir)
ner_path = os.path.join(prj_dir, "data/model/ner/product_bert")
dic_path = os.path.join(prj_dir, "data/dict/dict1.txt")

# 加载用户自定义词典
custom_dict = {}
with open(dic_path, "r", encoding="utf-8") as f:
    for line in f:
        word, tag = line.strip().split()
        custom_dict[word] = tag  # 例如: 借样 NN
tokenizer.dict_force = custom_dict

pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
ner_model = hanlp.load(ner_path)

# 建立 pipeline
pipeline = hanlp.pipeline() \
    .append(tokenizer, output_key='tok') \
    .append(pos_tagger, input_key='tok', output_key='pos') \
    .append(ner_model, input_key='tok', output_key='ner')


def ner_predict(text: str):
    skip_pos = {"CC", "PU", "DEG", "DEC", "DEV"}  # 排除的詞性
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
            if pos_tags[i] not in skip_pos:  # 只有非排除詞性才標註
                ner_tags[i] = entity_type

    # 增加规则：下文是"对账单"，前一个token标为CUSTOMER
    business_rules = {
        "对账单": (["O", "AGENT"], "CUSTOMER"),
        "借样": (["O", "CUSTOMER"], "AGENT"),
    }
    for i, tok in enumerate(tokens):
        if tok in business_rules:
            allowed_prev, target_ner = business_rules[tok]
            if i > 0 and ner_tags[i - 1] in allowed_prev:
                ner_tags[i - 1] = target_ner
            ner_tags[i] = target_ner  # 当前 token 也标注

    # JSON 輸出
    output = [
        {"token": t, "pos": p, "ner": n}
        for t, p, n in zip(tokens, pos_tags, ner_tags)
    ]
    return output
