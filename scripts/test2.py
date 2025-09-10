from app.pipeline import ner_predict

# 範例
if __name__ == "__main__":
    text = "查询楊馮凱对账单"
    ner_output = ner_predict(text)  # 先拿逐 token 結果
    print(ner_output)
    text = "查询楊馮凱X对账单"
    ner_output = ner_predict(text)  # 先拿逐 token 結果
    print(ner_output)