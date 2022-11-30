#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-11-24 10:00
# @Author   : paperclub
# @Desc     : paperclub@163.com




""" 获取知末关键字 """

import re
import json


def load_json(file_in):
	return json.load(open(file_in, 'r', encoding='utf-8', errors='ignore'))


def docment_to_sentences(text):
	""" 拆分句子 """
	text = re.sub('([。！？；\?!])([^"‘])', r"\1\n\2", text) # 断句
	text = re.sub('(\…{2}|\.{6}|[\.|;]\s)([^”’])', r"\1\n\2", text) # 省略号、英文句号、分号
	text = re.sub('([。！？\?!][”’])([^，。！？\?!])', r"\1\n\2", text)
	text = text.rstrip() # 段尾如果有多余的\n就去掉它

	return text.split("\n")


def load_stopwords():
	""" 加载停止词 """
	stopwords = [w.strip() for w in open("./process/stopwords.txt", 'r').readlines()]
	return stopwords


def sent_to_words(sentence: str):
	""" 句子拆分词 """
	words = []
	out = ""
	reg = r'[\d|,|，|、|·|•|“|"|!|~|你|我|她|他|说|这|着|那|哪|是|的|得|了|和|在|有|村|街道|镇|县|市|省|公司|酒店|样板间|集团|(主|次)卧|最(小|大)|(大|小)学]*'
	conditions = [':', '：', '|', '/', '┃', '丨', '｜', '／']
	res = re.search(rf'[{"|".join(conditions)}]', sentence)

	if res:
		words = re.split(f'[{"|".join(conditions)}]', sentence)
		words = [w.strip() for w in words if (w and 1 < len(w.strip().replace(" ", '')) < 20 ) and
		         (w not in STOPWORDS) and len(list(filter(bool,re.findall(reg, w)))) == 0 ]
		if words:
			out = sentence

	return words, out



def docment_to_words():
	""" 从文章中获取的初级关键字 """

	words = set()
	sentences = set()
	for i, doc in enumerate(zm_data):
		url = doc['url']
		detail = doc['detail']
		title = doc['title']
		detail_texts = [ x for x in detail if x and not x.startswith("http")]

		if detail_texts:
			for paragraph in detail_texts:
				sents = docment_to_sentences(paragraph) # 拆分句子

				for s in sents:
					s = s.strip()
					res, s2 = sent_to_words(s)
					if res:
						words.update(res)
						if s2:
							sentences.add(s2)
						print("res: ", res)
						print("---------------------------")

	words = list(words)
	words = sorted(words)
	sentences = list(sentences)
	if words:
		print("\n".join(words), file=open(raw_wordsfile, 'w', encoding='utf-8'))

	if sentences:
		print("\n".join(sentences), file=open(raw_sentsfile, 'w', encoding='utf-8'))


def is_contains_chinese(strs):
	"""检验是否含有中文字符"""
	for _char in strs:
		if '\u4e00' <= _char <= '\u9fa5':
			return True
	return False


def use_chinese(lines):

	###### 中文词筛选
	ignores = ['“新生”', '△方影', '一', '一个', '丁', '七', '万', '三', '上', '上图', '下', '丌', '不', '专长', '且', '世',
	            '丘', '东', '两', '严', '中', '丰', '串', '临', '临时展厅设计', '丹', '为', '丽', '举', '久', '义', '乌', '乐',
	            '乔', '乜', '九', '习', '二', '于', '云', '五', '井', '亢', '交通', '人', '仁', '仇', '仉', '从', '令', '以肉之名',
	            '仰', '仲', '任', '伊', '伍', '伏', '传承文化符号', '伦', '伯', '但', '何', '佘', '余', '余霖', '佛山', '作为',
	            '作品描述', '佴', '侯', '促', '俄', '保利', '保定', '保护', '俞', '俟', '倪', '傅', '傍', '储', '儿', '元', '充',
	            '兆', '党', '全', '全部', '全面', '公', '六', '兰', '关', '关于', '关键词', '养', '冀', '冉', '农', '冯', '况',
	            '冶', '冷', '凌', '凤', '刁', '刘', '利', '别', '加密', '劳', '勾', '包', '北', '匡', '千', '华', '卓', '单',
	            '南', '卜', '卞', '卢', '卫', '印', '危', '厉', '厍', '双', '叔', '古', '台', '台湾', '史', '叶', '司', '吉',
	            '后', '向', '吕', '吧', '吴', '周', '呼', '和', '咸', '唐', '商', '喻', '嗅觉', '四', '国', '图片', '堵', '壤',
	            '夏', '夔', '太', '夹', '奚', '姚', '姜', '姬', '娄', '子', '孔', '孙', '孟', '季', '宁', '宇', '安', '宋', '宓',
	            '宗', '官', '客厅', '客户', '宣', '宦', '宫', '宰', '家', '容', '宿', '寇', '富', '寿', '封', '尉', '尚', '尤',
	            '尹', '尼尔', '居', '屈', '展厅设计', '展览', '屠', '山', '岑', '岳', '崔', '嵇', '州', '巢', '左', '巩', '巫',
	            '巴', '帅', '师', '帕', '帝', '席', '常', '干', '平', '并', '幸', '广', '广东', '广州', '庄', '应', '庞', '康',
	            '庾', '廉', '廖', '延', '弓', '弘', '张', '强', '归', '彭', '徐', '徒', '微', '怀', '怡', '恒', '恩', '悠', '悦',
	            '悬', '惠', '想', '意见', '慎', '慕', '慧', '戈', '戎', '成', '成都', '或', '戚', '戴', '房', '房屋信息', '扈',
	            '托', '扬', '扶', '抱', '拓', '拳', '拿', '挪', '振', '捷', '掌', '描', '摩', '攀', '支', '改造效果对比', '政',
	            '故', '敖', '整个', '文', '斯', '新加坡', '新西兰', '方', '於', '施', '无', '日', '早', '旭辉', '时', '时代', '时光',
	            '昆', '昌', '明', '易', '昝', '星', '春', '晁', '晋', '晏', '晓', '普', '景', '暨', '暴', '曲', '曹', '曾', '有',
	            '木', '朱', '朴', '权', '李', '李明扬', '杜', '束', '杨', '杭', '松', '林', '柏', '查', '柯', '柳', '柴', '栾',
	            '桂', '桑', '桓', '梁', '梅', '楚', '樊', '欧', '正', '步', '武', '歪', '殳', '段', '殷', '毋', '每', '比', '比赛',
	            '毕', '毛', '氟', '水', '永', '汝', '江', '池', '汤', '汪', '汲', '沃', '沈', '沉', '沙', '沟', '河', '治', '泉',
	            '法', '波兰', '洪', '浙江', '浦', '海', '涂', '淳', '温', '游', '湛', '滑', '滕', '满', '漆', '潘', '澹', '濮',
	            '焦', '熊', '燕', '父', '牛', '牟', '牧', '狄', '狐', '王', '王丹丹', '班', '琴', '璩', '甄', '甘', '生', '用户',
	            '甫', '田', '由来', '申', '白', '百', '的', '皇', '皮', '益', '盖', '盛', '相', '督', '瞿', '石', '祁', '祖',
	            '祝', '禄', '禹', '离', '秋', '秦', '程', '穆', '空', '窦', '章', '童', '端', '竺', '符', '简', '简介', '管',
	            '籍', '米', '糜', '索', '红', '纪', '终', '经', '维', '缑', '缪', '罗', '羊', '羿', '翁', '翟', '耿', '聂', '胡',
	            '胥', '能', '脸', '臧', '自然', '舌', '舒', '航区', '良', '艾', '芮', '花', '苍', '苏', '苗', '英文名称', '范', '茅',
	            '茶', '茹', '荀', '荆', '荣', '莘', '莫', '萧', '葛', '董', '蒋', '蒙', '蒯', '蒲', '蓝', '蓟', '蓬', '蔚', '蔡',
	            '蔡保兵', '蔺', '薄', '薛', '虞', '融', '衡', '袁', '裘', '裴', '褚', '西', '西班牙', '解', '訾', '詹', '计', '许',
	            '诸', '谈', '谢', '谭', '谷', '贝', '贡', '贲', '费', '贺', '贾', '赏', '赖', '赫', '赵', '越', '跋', '路', '车',
	            '轩', '辕', '辛', '边', '连', '迟', '逄', '通', '逯', '邓', '邢', '那', '邬', '邰', '邱', '邴', '邵', '邹', '郁',
	            '郈', '郎', '郏', '郑', '郗', '郜', '郝', '郤', '郦', '郭', '都', '都市蓝', '鄂', '鄢', '酆', '里', '重庆', '金',
	            '钟', '钦', '钭', '钮', '钱', '锐', '长', '门', '闫', '闵', '闻', '闾', '阅', '阎', '阙', '阚', '阮', '阳', '阴',
	            '阿', '陆', '陈', '陕', '陶', '隆', '隗', '雁', '雅', '雍', '雕', '雪', '雷', '霍', '青', '静', '靳', '鞠', '韦',
	            '韩', '韶', '项', '项目简介', '顺', '须', '顾', '颛', '颜', '飞', '饶', '香', '马', '马来西亚', '驷', '骆', '高',
	            '鬱', '魏', '魔', '鱼', '鲁', '鲍', '鲜', '鸿', '鹿', '麓', '麦', '麻', '黄', '黎', '黑', '鼎', '齐', '龙', '龚']


	reg = r"[a-zA-Z0-9|*|\W|\.|\[|\|\\|、|_|-|©|à|——|‘|'|▲|▼|△|▽|◆|●|❒|《|》|「|」|【|】|（|）|(|)|;|=|<|é]*|" \
	      r"á|Ö|"

	words = set()
	for i, line in enumerate(lines):
		line = line.strip()
		is_chinese = is_contains_chinese(line)
		if is_chinese:
			line = re.sub('-|>|\+|#|&|@', '', line)
			overlap = any(r in line for r in ignores )
			ws = line.split()
			if not overlap:
				for w in ws:
					w = "".join(re.sub(reg, "", w))
					w = "".join(re.findall(r'[\u4e00-\u9fa5]', w))
					if len(w) > 1 and w not in SCHEMA_WORDS:
						words.add(w)
	words = sorted(list(words))
	return words



STOPWORDS = load_stopwords()
zm_data = load_json("./data/second/zm.json")
raw_wordsfile = "./w.txt"
raw_sentsfile = "./sents.txt"
SCHEMA_WORDS = []
for _k, _v in load_json("./project_templates1.1a.json")['project_templates'].items():
	SCHEMA_WORDS.append(_k)
	SCHEMA_WORDS.extend(_v)


# docment_to_words()
def is_contains_english(str):
    """ 检测是否含有英文字符 """
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False

words = set()




userfull = set()
with open(raw_sentsfile, 'r') as f:
	conditions = [':', '：', '|', '/', '┃', '丨', '｜', '／']
	for line in f.readlines():
		line = line.strip()

		if any([c in line for c in conditions]):
			syninfo = re.split(rf'[{"|".join(conditions)}]', line)
			if len(syninfo) != 2: continue
			if len(syninfo[1]) > 20 or len(syninfo[1]) < 2 : continue
			syn = syninfo[0]
			if syn and 10 > len(syn) > 1:
				syn = syn.strip()
				if syn:
					if is_contains_chinese(syn) and not is_contains_english(syn):
						syn2 = "".join(re.findall(r"\w", syn))
						if syn2 not in SCHEMA_WORDS:
							words.add(syn + " ==> " + line)
							userfull.add(syn)


print("\n".join(list(userfull)), file=open("candidates.txt", 'w', encoding='utf-8'))


