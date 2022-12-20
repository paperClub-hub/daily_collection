#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-12-07 10:35
# @Author   : paperclub
# @Desc     : paperclub@163.com



import re
from collections import defaultdict

def get_time(strs: str):
	""" 时间处理 """

	def _date_unit():
		" 月份时间转化 "

		# 英文 month映射
		month_dict = {'January': '1', 'Jan.': '1', 'February': '2', 'Feb.': '2', 'March': '3', 'Mar.': '3',
		              'April': '4', 'Apr.': '4', 'May': '5', 'May.': '5', 'June': '6', 'Jun.': '6', 'July': '7',
		              'Jul.': '7',
		              'August': '8', 'Aug.': '8', 'September': '9', 'Sep.': '9', 'Sept.': '9', 'October': '10',
		              'Oct.': '10',
		              'November': '11', 'Nov.': '11', 'December': '12', 'Dec.': '12'}

		# 英文 day映射
		_day_dict = {'1st': '1', '21st': '21', '31st': '31', '2nd': '2', '22nd': '22', '3rd': '3', '23rd': '23'}
		day_dict = dict([str(x), str(x)] for x in range(1, 32))
		day_dict.update(_day_dict)
		day_dict.update(dict([f"{i}th", str(i)] for i in range(1, 32) if str(i) not in list(_day_dict.values())))
		day_dict = dict(sorted(day_dict.items(), key=lambda d: len(d[0]), reverse=True))  # day顺序：先英文day，再纯数字day

		month_format = defaultdict(list)
		for k, vs in month_dict.items():
			if k not in month_format:
				month_format.update({k: month_dict.get(k)})
			if k.upper() not in month_format:
				month_format.update({k.upper(): month_dict.get(k)})
			elif k.lower() not in month_format:
				month_format.update({k.lower(): month_dict.get(k)})

		del month_dict, _day_dict

		return month_format, day_dict


	def _normalization(strs: str):
		"""
		时间归一化入口： 将时间格式统一
		"""

		def _std_time_normalize(strs: str) -> str:
			#  标准时间归一化处理
			ymd_reg = r'[\d]+'
			year, month, day = '', '', ''
			res = re.findall(ymd_reg, strs, re.IGNORECASE)
			if len(res) == 1:  # 纯数字，如20221201，202261
				res = res[0]
				year = res[:4]
				if len(res) > 4:
					if int(res[4:6]) <= 12:
						month = res[4:6]
						day = res[6:]
					else:
						month = res[4:5]
						day = res[5:]

			elif len(res) > 1:  # 含有其他分割符
				year = res[0][:4]
				month = res[1]
				if len(res) > 2:
					day = res[-1]

			if year:
				year += '年'
			if month:
				month += '月'
			if day:
				day += '日'

			del res
			return ''.join(list(filter(bool, [year, month, day])))


		# 英文月份、日
		month_dict, day_dict = _date_unit()
		mo_ens = '|'.join(list(month_dict.keys()))
		da_ens = '|'.join(list(day_dict.keys()))

		# 校验规则：
		# 标准格式：匹配‘2021年6月1日’，或‘2021年6月’，‘2021年’或‘2021’，‘20210601’，‘202106’
		standard_reg = r'(^(?:19|20)\d{2}(年|\.|-|/)?(([0]?\d|1[012])(月(份)?|\.|-|/)?)?(([012]?\d|3[01])(日|号)?)?)$'
		# 英文日月年或月年：匹配'12th SEPTEMBER 2015', 'SEPTEMBER 2015', '18 December 2022'
		dmy_en_reg = '((' + da_ens + ')?[\s]?(' + mo_ens + ')[\s]?(' + '\d{4})' + ')'
		# 英文年月日或年月：匹配'2015 SEPTEMBER 12th'，
		ymd_en_reg = '(' + '(\d{4})[\s]?(' + mo_ens + ')[\s]?(' + da_ens + ')?)'

		# 规格化处理
		normalized_time_str = ''
		standard_res = re.search(standard_reg, strs, re.IGNORECASE)
		dmy_en_res = re.search(dmy_en_reg, strs)
		ymd_en_res = re.search(ymd_en_reg, strs)

		if standard_res:  # 标准年月日
			normalized_time_str = _std_time_normalize(strs)
		else:
			if dmy_en_res:  # 英文日月年
				res = re.findall(dmy_en_reg, strs, re.IGNORECASE)
				if res:
					res = res[0][1:]
					_day = day_dict.get(res[0], '') if res[0] else ''
					_month = month_dict.get(res[1], '') if res[1] else ''
					_year = re.findall(r'\d{4}', strs)[0]
					en_date = '-'.join(list(filter(bool, [_year, _month, _day])))
					normalized_time_str = _std_time_normalize(en_date)
					del _day, _month, _year

			elif ymd_en_res:  # 英文年月日
				res = re.findall(ymd_en_reg, strs, re.IGNORECASE)
				if res:
					res = res[0][1:]
					_year = re.findall(r'\d{4}', strs)[0]
					_month = month_dict.get(res[1], '') if res[1] else ''
					_day = day_dict.get(res[-1], '') if res[-1] else ''
					en_date = '-'.join(list(filter(bool, [_year, _month, _day])))
					normalized_time_str = _std_time_normalize(en_date)
					del _day, _month, _year

		return normalized_time_str

	def _get_time(strs: str):
		# 获取时间表达式
		month_dict, day_dict = _date_unit()
		mo_ens = '|'.join(list(month_dict.keys()))

		# 年月日格式
		ye_n = '(([12]?\d{2,3})|(一|二|三|四|五|六|七|八|九|零|〇|○|0){4}?)'  # 年份数字格式
		mo_n = '([0]?\d|1[012])'  # 月份数字格式
		mo_c = '(元|正|腊|一|二|三|四|五|六|七|八|九|十(一|二)?)'  # 月份汉字格式
		da_n = '([012]?\d|3[01])(th|nd|st|rd)?'  # 日数字格式
		ymd_n = r'(^(?:17|18|19|20)\d{2}' + '(\d{1,2})?' + '(\d{1,2})?)'  # 纯数窜字年月日或年月(20221219, 2022)
		ymd_gap = '[\-\~— ～\.\/]{1,2}'  # 年跨度格式

		# 组合年月日规则
		ymd_pattern_1 = '(' + ye_n + '[\s]?((上|下)半)?年(初|底|末|度|代|(上|下)半年)?)((' + mo_n + '|' + mo_c + ')月(份|底|初)?)?(' + da_n + '[日号])?'  # 带中文格式的年月日
		ymd_pattern_2 = '^(' + ye_n + ymd_gap + mo_n + '(' + ymd_gap + da_n + ')?)$'  # 数值年月日格式或年月格式
		ymd_pattern_3 = '((' + da_n + '[\s])?(' + mo_ens + ')[\s](' + ye_n + '))$'  # 英文日月年格式，或月年格式
		ymd_pattern_4 = '((' + ye_n + '[\s]?(Year)?(' + mo_ens + ')[\s]?)(' + da_n + ')?)'  # 英文年月日格式，或年月格式
		ymd_pattern_5 = '(' + '(([12]?\d|(二)?十(一|二|三|四|五|六|七|八|九)?)世纪)?((\d0|(一|二|三|四|五|六|七|八|九)十)年代)?(初|末)?' + ')$'  # 世纪，年代
		season_pattern = '((春|夏|秋|冬){1,2}(季|天|日)|(第)?(一|二|三|四)(季度)(末)?)'
		# 时间规则汇总
		reg = r'(' + '|'.join([ymd_pattern_1, ymd_pattern_2, ymd_pattern_3, ymd_pattern_4, ymd_pattern_5, ymd_n, season_pattern]) + ')'

		time_match = re.search(reg, strs, re.IGNORECASE)

		time_info = ''
		if time_match:
			time_info = time_match.group()

		return time_info

	time_info = _get_time(strs)
	time_str = _normalization(time_info)

	# print("input: ", strs, ", 转化结果=>>> ", time_str)

	return time_str



ts = [
	'2022年6月21日',
	'2022',
	'2022',
	'20220621',
	'202206',
	'202261',
	'2022-10',
	'2022-01',
	'2022-06-21',
	'2022/06/21',
	'2022-6-1',
	'12th SEPTEMBER 2022',
	'SEPTEMBER 2022',
	'18 December 2022',
	'18th December 2022',
	'2022 SEPTEMBER 12th',
	'2022 SEPTEMBER 12',
	'2021-12-27',
	'2021-12',
	'2017.11.14',
	'2017.11',
  ]

for t in ts:
	out = get_time(t)
	print(f"Input: {t},   转化结果=>>>  {out}")