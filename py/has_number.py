
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Author   : paperclub
# @Desc     : paperclub@163.com

import re


""" 检查字符串中是否有数值型数据"""

reg = '([\d|一|二|三|四|五|六|七|八|九|十|壹|贰|叁|弎|仨|肆|伍|陆|柒|捌|玖|俩|两|零|百|千|万|亿|兆|拾|佰|仟|萬|億]+)'
reg += "|(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?Dec(ember)?)"
reg +="|(zero|one|two|three|four|five|six|seven|eight|nine)"

patten = re.compile(reg)


text = ["今天星期三", "电话119", "one boy"]

for x in text:
	state = patten.search(x)
	if state:
		print(f"{x}: =>  {state.group()}")

