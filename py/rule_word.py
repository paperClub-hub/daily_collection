#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-11-07 10:35
# @Author   : paperclub
# @Desc     :


import re

w = "项目名称"
reg = rf"([【]?[\s]?{w}[\s]?[】]?"

a = 1
b = a + 10
reg += r"([\s|\w|\W]?){"
reg += rf"{a},{b}"
reg += r"}"
reg += r"(\。|\.\s|\；|\;|$))"


text = """项目名称 小区拆迁房翻新。 小区绿化很漂亮。"""

res = re.search(reg, text)


if res:
	print("结果： ==》》》 ", res.group())
else:
	print("无结果")