# 範例測試
from app.cn_util import zh_conv

text1 = "汉字简体转繁体"
text2 = "漢字繁體轉簡體"

print(zh_conv(text1))          # 自動判斷
print(zh_conv(text2))          # 自動判斷
print(zh_conv(text1, 'zh-tw'))  # 強制轉繁體
print(zh_conv(text2, 'zh-cn'))  # 強制轉簡體
