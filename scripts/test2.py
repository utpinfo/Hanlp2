from app.pipeline import ner_predict

# 範例
if __name__ == "__main__":
    text = "查詢上海倉海裡嗯库存"
    ner_output = ner_predict(text)  # 先拿逐 token 結果
    print(ner_output)