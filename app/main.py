from fastapi import FastAPI
from pydantic import BaseModel
from .pipeline import ner_predict

app = FastAPI(
    title="ERP NLP API",
    description="這個 API 提供中文文本的 NER 分析",
    version="1.0.0"
)

class TextRequest(BaseModel):
    text: str

@app.post(
    "/ner",
    summary="命名實體識別",
    description="輸入中文文本，返回每個詞的分詞、詞性和 NER 標籤"
)
def ner_api(req: TextRequest):
    """
    POST /ner
    輸入 JSON: {"text": "查詢ME&CITY4支裝展架（太陽鏡）庫存"}
    返回 JSON: [{"token": "ME", "pos": "NR", "ner": "PRODUCT"}, ...]
    """
    return ner_predict(req.text)
