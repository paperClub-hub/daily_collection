
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : paperclub
# @Desc     : paperclub@163.com


def is_all_chinese(strs):
    """ 判断字符串全为中文 """
    # reg = '~`!#$%^&*()_+-=|\';":/.,?><~·！@[\\]【\\】#￥%……&*（）——+-=“：’；、。，？》《{}'
    # strs = re.sub(rf"[{reg}|\s]+", "", strs) # 去除标点符号及空格, 等价： re.sub(r"[%s|\s]+" %reg, "", strs)
    # for _char in strs:
    #     if not '\u4e00' <= _char <= '\u9fa5':
    #         return False
    #
    # return True

    reg = '~`!#$%^&*()_+-=|\';":/.,?><~·！@[\\]【\\】#￥%……&*（）——+-=“：’；、。，？》《{}'
    reg += '|\s|\W|\d'
    strs = re.sub(rf"[{reg}]+", "", strs)

    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False

    return True


def is_all_chinese1(strs):
    """ 判断字符串全为中文 """
    """ 速度慢 """
    reg = '~`!#$%^&*()_+-=|\';":/.,?><~·！@[\\]【\\】#￥%……&*（）——+-=“：’；、。，？》《{}'
    strs = re.sub(rf"[{reg}|\s]+", "", strs) # 去除标点符号及空格, 等价： re.sub(r"[%s|\s]+" %reg, "", strs)

    identify = list(map(lambda s: '\u4e00' <= s <= '\u9fa5', strs))

    return all(identify)



def is_contains_chinese(strs):
    """检验是否含有中文字符"""
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False



def is_all_english(strs):
    """ 检测是否全是英文字符 """
    # reg = '~`!#$%^&*()_+-=|\';":/.,?><~·！@[\\]【\\】#￥%……&*（）——+-=“：’；、。，？》《{}'
    # strs = re.sub(rf"[{reg}|\s]+", "", strs) # 去除标点符号及空格, 等价： re.sub(r"[%s|\s]+" %reg, "", strs)

    reg = '~`!#$%^&*()_+-=|\';":/.,?><~·！@[\\]【\\】–#￥%……&*（）——+-=“：’；、。，？》《{}|\s|\W'
    strs = re.sub(f"[{reg}]*", "", strs)

    for i in strs:
        if i not in string.ascii_lowercase + string.ascii_uppercase:
            return False
    return True

def is_contains_english(str):
    """ 检测是否含有英文字符 """
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False


input1 = """我爱中国"""
input2 = """paperclub"""

print("input1是否全为中文：", is_contains_chinese(input1))
print("input1是否包括中文：", is_contains_chinese(input1))
print("input1是否全为英文：", is_all_english(input1))
print("input1是否包括英文：", is_contains_english(input1))

print("input2是否全为中文：", is_contains_chinese(input2))
print("input2是否包括中文：", is_contains_chinese(input2))
print("input2是否全为英文：", is_all_english(input2))
print("input2是否包括英文：", is_contains_english(input2))