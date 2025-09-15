from app.pipeline import ner_predict

# 範例
if __name__ == "__main__":
    text = "查詢楊馮凱的借樣"
    ner_output = ner_predict(text)  # 先拿逐 token 結果
    print(ner_output)