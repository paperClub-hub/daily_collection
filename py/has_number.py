
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Author   : paperclub
# @Desc     : paperclub@163.com

import re


def is_numerical(word:str):
	""" 检查字符串中是否有数值型数据"""

	reg = '([\d|一|二|三|四|五|六|七|八|九|十|壹|贰|叁|弎|仨|肆|伍|陆|柒|捌|玖|俩|两|零|百|千|万|亿|兆|拾|佰|仟|萬|億]+)'
	reg += "|(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?Dec(ember)?)"
	reg +="|(zero|one|two|three|four|five|six|seven|eight|nine)"

	state = False
	vlaue = ""
	patten = re.compile(reg)
	res = patten.search(word)
	if res:
		state = True
		vlaue = res.group()

	return state, vlaue




text = ["今天星期三", "电话119", "one boy", '2023年，新冠终将称为过去式！', 'hello, paperClub', '今天的你， 是否比昨天快乐呢？ ']

for x in text:
	state, value = is_numerical(x)

	print(f"{x}: =>  is_numerical: {state}, value: {value}")

