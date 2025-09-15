# 範例測試
from app.cn_util import detect_chinese_type, zh_conv

text1 = "对账单"
text2 = "對帳單"

print(detect_chinese_type(text1))  # 自動判斷
print(detect_chinese_type(text2))  # 自動判斷
print(zh_conv(text1, 'zh-tw'))  # 強制轉繁體
print(zh_conv(text2, 'zh-cn'))  # 強制轉簡體
