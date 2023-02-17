#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2023-02-15 17:30
# @Author   : NING MEI
# @Desc     :


import re

def grid_search(text:str):
	""" 全面搜索候选，从长至短，较优 """
	length = len(text)
	for i in range(length):  # 控制总长，若想控制单字符的串也被返回考察，此时改为 length + 1
		for j in range(i):  # 控制偏移
			offset = [j, length - i + j + 1]
			sub_string = text[j: offset[1]]
			print("sub_string: ", sub_string, i, j, offset)



def grid_search2(text:str):
	""" 全面搜索候选，从长至短，较优 """
	offset = [0, 0]

	while offset[1]  < len(text):
		print("*******************")
		length = len(text)
		for i in range(length):
			for j in range(i):
				offset = [j, length - i + j + 1]
				sub_string = text[j: offset[1]]

				# 符合不某种条件退出
				if len(sub_string) > 3:
					print(sub_string)
					continue


def grid_search3(text:str):
	""" 全面搜索候选，从长至短，较优 """


	def func(text):
		#  功能示例
		length = len(text)
		for i in range(length):
			for j in range(i):
				try:
					offset = [j, length - i + j + 1]
					sub_string = text[j: offset[1]]
					# 符合某种条
					reg = '\d+'
					d = re.search(reg, sub_string).group()
					return offset, d
				except:
					continue

		return None, -1

	offset = [0, 0]
	bias = 0
	while offset[1] < len(text):
		offset, d = func(text[bias:])
		bias +=offset[1]

		print("d ==>>> ", d)
		if offset is not None:
			pass







text = "2023年春季"
# grid_search(text)
# grid_search2(text)
grid_search3(text)