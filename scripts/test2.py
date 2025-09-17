import os

import hanlp

from app.pipeline import ner_predict

# 範例
if __name__ == "__main__":
    text = "查詢上海倉海裡嗯库存"
    ner_output = ner_predict(text)  # 先拿逐 token 結果
    print(ner_output)

    # 加载训练好的模型
    """
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # 禁用 GPU
    classifier = hanlp.load('../data/model/intent/bert_base')
    test_sentences = ['查询DY01库存', '我要退貨']
    # 模型预测
    results = classifier.predict(test_sentences)
    # 输出结果
    for sent, label in zip(test_sentences, results):
        print(f"{sent} -> {label}")
    """
