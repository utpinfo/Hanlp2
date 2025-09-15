from opencc import OpenCC

"""
text1 = "汉字简体转繁体"
text2 = "漢字繁體轉簡體"

print(detect_chinese_type(text1)) # 自動判斷
print(zh_conv(text1, 'zh-tw'))  # 強制轉繁體
print(zh_conv(text2, 'zh-cn'))  # 強制轉簡體
"""
# 初始化 OpenCC 对象
cc_s2t = OpenCC('s2t.json')  # 简→繁
cc_t2s = OpenCC('t2s.json')  # 繁→简


def detect_chinese_type(text: str) -> str:
    """
    判斷文本是簡體還是繁體
    :param text: 中文文本
    :return: 'zh-cn' 簡體, 'zh-tw' 繁體
    """
    to_trad = cc_s2t.convert(text)
    to_simp = cc_t2s.convert(text)

    # 計算與原文差異比例
    diff_trad_ratio = sum(a != b for a, b in zip(text, to_trad)) / max(len(text), 1)
    diff_simp_ratio = sum(a != b for a, b in zip(text, to_simp)) / max(len(text), 1)

    if diff_trad_ratio < diff_simp_ratio:
        return 'zh-tw'
    else:
        return 'zh-cn'


def convert_chinese(text: str, target: str) -> str:
    """
    將文本轉換為指定版本
    :param text: 中文文本
    :param target: 'zh-cn' 簡體, 'zh-tw' 繁體
    :return: 轉換後文本
    """
    if target == 'zh-cn':
        return cc_t2s.convert(text)
    elif target == 'zh-tw':
        return cc_s2t.convert(text)
    else:
        raise ValueError("target 必須是 'zh-cn' 或 'zh-tw'")


def zh_conv(text: str, target: str = 'auto'):
    """
    判斷中文文本類型並轉換
    :param text: 中文文本
    :param target: 'zh-cn' 簡體, 'zh-tw' 繁體, 'auto' 自動判斷並轉成相反版本
    :return: 轉換後文本
    """
    original_type = detect_chinese_type(text)

    if target == 'auto':
        # auto 模式，返回“反转”版本
        if original_type == 'zh-cn':
            return convert_chinese(text, 'zh-tw')
        else:
            return convert_chinese(text, 'zh-cn')
    else:
        return convert_chinese(text, target)


# 範例
if __name__ == "__main__":
    text1 = "汉字简体转繁体"
    text2 = "漢字繁體轉簡體"

    print(detect_chinese_type(text1))  # 自動判斷
    print(detect_chinese_type(text2))  # 自動判斷
    print(zh_conv(text1, 'zh-tw'))  # 強制轉繁體
    print(zh_conv(text2, 'zh-cn'))  # 強制轉簡體
