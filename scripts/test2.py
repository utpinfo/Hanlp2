from app.pipeline import ner_predict

# 範例
if __name__ == "__main__":
    text = "查询海俪恩库存数量"
    ner_output = ner_predict(text)  # 先拿逐 token 結果
    print(ner_output)