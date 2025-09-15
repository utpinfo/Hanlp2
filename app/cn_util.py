from opencc import OpenCC
"""
text1 = "汉字简体转繁体"
text2 = "漢字繁體轉簡體"

print(zh_conv(text1))          # 自動判斷
print(zh_conv(text2))          # 自動判斷
print(zh_conv(text1, 'zh-tw'))  # 強制轉繁體
print(zh_conv(text2, 'zh-cn'))  # 強制轉簡體
"""
def zh_conv(text: str, target: str = 'auto'):
    """
    判斷中文文本是簡體還是繁體，並轉換到目標版本
    :param text: 中文文本
    :param target: 'zh-cn' 簡體, 'zh-tw' 繁體, 'auto' 保持原文
    :return: 轉換後文本 或 (原文, 原始類型)
    """
    cc_s2t = OpenCC('s2t.json')
    cc_t2s = OpenCC('t2s.json')

    to_trad = cc_s2t.convert(text)
    to_simp = cc_t2s.convert(text)

    # 計算與原文差異比例
    diff_trad_ratio = sum(a != b for a, b in zip(text, to_trad)) / max(len(text), 1)
    diff_simp_ratio = sum(a != b for a, b in zip(text, to_simp)) / max(len(text), 1)

    # 判斷原文
    if diff_trad_ratio < diff_simp_ratio:
        original_type = 'zh-tw'
    else:
        original_type = 'zh-cn'

    # 根據 target 返回
    if target == 'zh-cn':
        return to_simp
    elif target == 'zh-tw':
        return to_trad
    else:  # auto
        return text, original_type