#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-12-07 10:35
# @Author   : paperclub
# @Desc     : paperclub@163.com



import re

def get_area(strs: str):
	"""
	面积数值处理与提取
	Args:
		strs:

	Returns:

	示例：
		text= Sunshine---58平米, res =>>> 58平方米
		text= 六十九平米, res =>>> 六十九平方米
		text= -98㎡, res =>>> 98平方米
		text= -56㎡, res =>>> 56平方米
		text= 晴·89㎡, res =>>> 89平方米
		text= 148.5㎡, res =>>> 148.5平方米
		text= 800平方尺, res =>>> 800平方尺
		text= 800方尺, res =>>> 800方尺
		text= 10000+㎡, res =>>> 10000+平方米
		text= 2800㎡平面, res =>>> 2800平方米
		text= 120721方, res =>>> 120721平方米
		text= 8,200平方米, res =>>> 8200平方米
		text= 橙·109㎡, res =>>> 109平方米
		text= 125m2+, res =>>> 125平方米
		text= 1+1◥119m², res =>>> 119平方米
		text= 110,000平方, res =>>> 110000平方米
		text= 2800㎡平面, res =>>> 2800平方米
		text= 10000+㎡, res =>>> 10000+平方米
		text= 115m2, res =>>> 115平方米
		text= 980万平方公里, res =>>> 980万平方公里
	"""

	def _area_unit():
		""" 单位字典更新 """
		unit_dict = {"平": "平方米", "坪": "平方米", "平米": "平方米", "平方米": "平方米", "方": "平方米", "平方": "平方米",
		             "坪方": "平方米", "㎡": "平方米", "m²": "平方米", "M²": "平方米", "M2": "平方米", "м²": "平方米",
		             "М2": "平方米", "sqm": "平方米", 'M平方': "平方米", "万平": "万平方米", "万平方": "万平方米", "万平米": "万平方米",
		             "平方英尺": "平方英尺", "sq ft": "平方英尺", "sqft": "平方英尺"}

		dic_formt = {}
		for k, v in unit_dict.items():
			if k not in dic_formt:
				dic_formt.update({k: unit_dict.get(k)})
			if k.upper() not in dic_formt:
				dic_formt.update({k.upper(): unit_dict.get(k)})
			elif k.lower() not in dic_formt:
				dic_formt.update({k.lower(): unit_dict.get(k)})

		return dic_formt

	# 面积匹配规则
	_area_units = r"(十|百|千|万|亿)?(平(方)?(千)?(分)?(厘)?(米|尺|方尺|英尺)|平(方公里|方)?|方(尺)?|坪|M平方|英寸|km²|hm²|㎡|M²|M2|м²|М2|dm²|cm²|mm²|(公)?亩|(公)?顷|英尺|sq ft|sqm|metre(s)?|(square meter))"
	reg = r"([\d]+|[\d]+[.|,][\d]+)(\+)?(\s)?"
	reg += _area_units
	reg += rf'|((零|一|二|三|四|五|六|七|八|九)?(十|百|千|万|亿)?(\s)?(零|一|二|三|四|五|六|七|八|九)?)(\s)?{_area_units}'

	# 获取数值
	reg_digit = r'-?\d+\.?\,?\+?\d*|((零|一|二|三|四|五|六|七|八|九)?(十|百|千|万|亿)?(\s)?(点|零|一|二|三|四|五|六|七|八|九)?)'
	area_match = re.search(reg, strs, re.IGNORECASE)
	area_match = area_match.group() if area_match else ''
	# 面积单位处理
	unit_dict = _area_unit()

	area_info = ''
	if area_match:
		area_match = re.sub(r"[\s|\,|\，]", "", area_match)
		area = re.search(reg_digit, area_match).group()

		if area:
			unit = area_match.replace(area, '')
			unit = unit_dict.get(unit) if unit in unit_dict else unit
			area_info = f"{area}{unit}"


	return area_info



texts = [
		'Sunshine---58平米',
		'六十九 平米',
		'-98㎡',
		'- 56㎡',
		'晴·89㎡',
		'148.5㎡',
		'800 平方尺',
		'800方尺',
		'10000+㎡',
		'2800㎡平面',
		'120721方',
		'8,200平方米',
		'橙 · 109㎡',
		'125m2+',
		'1+1◥ 119m²',
		'110,000平方',
		'2800㎡平面',
		'10000+㎡',
		'115m2 ',
		'980万平方公里',
	]

if __name__ == '__main__':
	for t in texts:
	    t = t.replace(' ', '')
	    res = get_area(t)
	    print(f"{t},  res = >  {res}")