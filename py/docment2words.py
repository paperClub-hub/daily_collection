#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ Date    : 2023/1/29 9:55
# @ Author  : paperClub
# @ Email   : paperclub@163.com
# @ Site    :


import re

def text2words(text:str):
    """
    文档转单个字，可用于统计字数
    :param text: 文本
    :return: List
    """

    words = []

    punctuation_reg = r'~`!#$%^&*()_+-=|\';":/.,?><~·！@[\\]【\\】#￥%……&*（）——+-=“：’；、。，？》《{}'
    chinese_digit_reg = r'[\u4e00-\u9fa5]|[\d]+' # 中文及数字
    english_reg = r'[a-zA-Z]+' # 英文

    text = re.sub(punctuation_reg, ' ', text).lower()  # 去掉标点符号
    text = re.sub("\W", ' ', text)  # 去除特殊符号

    cn_words = re.findall(chinese_digit_reg, text)
    en_words = re.findall(english_reg, text)
    if cn_words:
        words.extend(cn_words)
        del cn_words
    if en_words:
        words.extend(en_words)
        del en_words
    del text

    return words




text = """呈现2D图像或数据的核心就是一个数据降维。我们知道每个词或图片都会有相应的隐含意义，这个意义也就是特征向量，比如 图1 第三行左侧的图像，我们看到一张有海水、蓝天、白云和桥面的图像，这些词都会通过向量的形式隐含的呈现出来，如果两张图像代表的内容足够相似或相近，那么他们的特征也同样会在空间上非常接近， 比如 图1 第三行的两张图像内容接近，因此在图2 中导致两张图像的空间向量重合在一起了。
"""

print("text: ", text)
print("words: ", text2words(text))
print("--------------------------------------")

text = "We're talking about a figure in the low hundreds."
print("text: ", text)
print("words: ", text2words(text))
print("--------------------------------------")


text = """
分享：一键完成老照片颜色修复，超级简单，支持网络图片和本地上传图片两种方法。paperClub发表于2022-09-12 10:54。
"""
print("text: ", text)
print("words: ", text2words(text))
print("--------------------------------------")

text = """Who Uses Infer? CodeAI JD.com Marks and Spencer Money Lover Netcetera OLA Sky Tile Vuo wolfSSL Does your project use Infer? Add it to this list witha pull request!"""
print("text: ", text)
print("words: ", text2words(text))
print("--------------------------------------")



