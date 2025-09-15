import json
import hanlp
import torch
import os
from app.cn_util import detect_chinese_type, zh_conv

"""
Service层
"""
# 設定線程數
ncpu = os.cpu_count()
if ncpu > 0:
    torch.set_num_threads(ncpu)
    torch.set_num_interop_threads(ncpu)

cur_dir = os.path.dirname(os.path.abspath(__file__))
prj_dir = os.path.dirname(cur_dir)
ner_path = os.path.join(prj_dir, "data/model/ner/product_bert")
dic_path = os.path.join(prj_dir, "data/dict")

# 加載分詞辭典
custom_dict_raw = []
for filename in os.listdir(dic_path):
    if filename.endswith(".json"):
        path = os.path.join(dic_path, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            custom_dict_raw.extend(data)

# 建立 custom_dict: token -> {"pos":..,"ner":..}
custom_dict = {item["token"]: {"pos": item["pos"], "ner": item["ner"]} for item in custom_dict_raw}
# 加載自定義分詞
tokenizer = hanlp.load('FINE_ELECTRA_SMALL_ZH')
tokenizer.dict_force = {item["token"]: item["ner"] for item in custom_dict_raw}

pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
ner_model = hanlp.load(ner_path)

# 建立 pipeline
pipeline = hanlp.pipeline() \
    .append(tokenizer, output_key='tok') \
    .append(pos_tagger, input_key='tok', output_key='pos') \
    .append(ner_model, input_key='tok', output_key='ner')


def ner_predict(text: str):
    skip_pos = {"CC", "PU", "DEG", "DEC", "DEV"}  # 排除的词性
    res = pipeline(text)
    tokens = res['tok']
    pos_tags = res['pos']
    ner_tags = ['O'] * len(tokens)

    # 1. 自定義字典覆盖Token/Ner (Support 繁體句子, 簡體字典)
    zh_cache = {}  # 用来缓存 token 的简体版本
    for i, tok in enumerate(tokens):
        # 先查原 token
        if tok in custom_dict:
            pos_tags[i] = custom_dict[tok]["pos"]
            ner_tags[i] = custom_dict[tok]["ner"]
        else:
            # 先看缓存
            if tok in zh_cache:
                tok_simp = zh_cache[tok]
            else:
                tok_simp = zh_conv(tok, 'zh-cn')
                zh_cache[tok] = tok_simp  # 保存到缓存
            # 用简体 token 查字典
            if tok_simp in custom_dict:
                pos_tags[i] = custom_dict[tok_simp]["pos"]
                ner_tags[i] = custom_dict[tok_simp]["ner"]

    # 2. Ner檢核處理
    for entity_text, entity_type, start, end in res['ner']:
        for i in range(start, end):
            if pos_tags[i] not in skip_pos and tokens[i] not in custom_dict:
                ner_tags[i] = entity_type

    # 3. 输出 JSON
    output = [
        {"token": t, "pos": p, "ner": n}
        for t, p, n in zip(tokens, pos_tags, ner_tags)
    ]
    return output
