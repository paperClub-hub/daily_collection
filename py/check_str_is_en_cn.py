
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-10-24 8:59

import string


def is_all_chinese(strs):
    """ 判断字符串全为中文 """

    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def is_contains_chinese(strs):
    """检验是否含有中文字符"""
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False



def is_all_english(strs):
    """ 检测是否全是英文字符 """
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