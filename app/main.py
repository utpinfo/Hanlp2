from fastapi import FastAPI
from pydantic import BaseModel

from .cn_util import zh_conv
from .pipeline import ner_predict

app = FastAPI(
    title="ERP NLP API",
    description="提供中文文本的 NER 分析和简繁转换",
    version="1.0.0"
)


# NER 请求模型
class NERRequest(BaseModel):
    text: str


# 简繁转换请求模型
class ZhConvRequest(BaseModel):
    text: str
    target: str = 'auto'  # 可选，默认自动判别


@app.post("/ner", summary="命名实体识别", description="输入中文文本，返回分词、词性和NER标签")
def ner_api(req: NERRequest):
    return ner_predict(req.text)


@app.post("/zh-conv", summary="简体繁体互转", description="输入中文文本，简体繁体互转")
def zh_conv_api(req: ZhConvRequest):
    """
    返回：
      - 如果 target='auto'，返回 {"text": 原文, "original_type": "zh-cn/zh-tw"}
      - 否则返回 {"text": 转换后的文本}
    """
    return {"text": zh_conv(req.text, req.target)}
