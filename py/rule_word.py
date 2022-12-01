#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-11-07 10:35
# @Author   : paperclub
# @Desc     :


import re


def word_map1():
	""" 字匹配方法示例1： 根据长度截取 """

	w = "项目名称"
	reg = rf"([【]?[\s]?{w}[\s]?[】]?"

	a = 1
	b = a + 10
	reg += r"([\s|\S]?){"
	reg += rf"{a},{b}"
	reg += r"}"
	reg += r"(\。|\.\s|\；|\;|$))"

	text = """项目名称： 小区拆迁房翻新。\n 小区绿化很漂亮。"""

	res = re.search(reg, text)

	if res:
		print("结果： ==》》》 ", res.group())
	else:
		print("无结果")



def word_map2():
	""" 字匹配方法示例2: 根据分拆标志符 """

	w = "项目名称"
	reg = rf"([【]?[\s]?{w}[\s]?[】]?"
	reg += r"([:|：|┃|/|／|│|丨|｜|︱]([\s\S\w\W]*?))" # 分割标志符 及尾随文字
	reg += r"(\。|\.\s|\；|\;|$))"  # 终止符

	text = """项目名称： 小区拆迁房翻新。\n 小区绿化很漂亮。"""

	res = re.search(reg, text)

	if res:
		print("结果： ==》》》 ", res.group())
	else:
		print("无结果")





if __name__ == '__main__':
	print("'方法1： ")
	word_map1()

	print("方法2： ")
	word_map2()