#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-12-07 10:35
# @Author   : paperclub
# @Desc     : paperclub@163.com



import re
from collections import defaultdict

def gettime(strs: str):
    """ 时间处理 """

    def _date_unit():
        " 月份时间转化 "

        # 英文 month映射
        month_dict = {'January':'1', 'Jan.': '1', 'February': '2', 'Feb.': '2', 'March': '3', 'Mar.': '3',
                      'April':'4', 'Apr.':'4', 'May':'5', 'May.':'5','June':'6', 'Jun.':'6', 'July':'7', 'Jul.':'7',
                      'August':'8', 'Aug.':'8',  'September':'9', 'Sep.':'9', 'Sept.':'9','October':'10','Oct.':'10',
                      'November': '11','Nov.': '11','December': '12','Dec.': '12' , 'may': '5'
                      }

        # 英文 day映射
        _day_dict = {'1st': '1', '21st': '21', '31st': '31', '2nd': '2', '22nd': '22', '3rd': '3', '23rd': '23'}
        day_dict = dict([str(x), str(x)] for x in range(1, 32))
        day_dict.update(_day_dict)
        day_dict.update(dict([f"{i}th", str(i)] for i in range(1, 32) if str(i) not in list(_day_dict.values())))
        day_dict = dict(sorted(day_dict.items(), key=lambda d: len(d[0]), reverse=True)) # day顺序：先英文day，再纯数字day

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

        def _std_time_normalize(strs: str)-> str:
            #  标准时间归一化处理
            ymd_reg = r'[\d]+'
            # ymd_reg = r'\d+'
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
        # standard_reg = r'(^(?:19|20)\d{2}(年(度)?|\.|-|/)?(([0]?\d|1[012])(月(份)?|\.|-|/)?)?(([012]?\d|3[01])(日|号)?)?)$'
        # standard_reg = r'(^(?:19|20)\d{2}(\s)?(年(度)?|\.|-|/)?(([0]?\d|1[012])(月(份)?|\.|-|/)?)?(([012]?\d|3[01])(日|号)?)?)$'
        standard_reg = r'(^[12]?\d{2,3}(\s)?(年(度)?|\.|-|/)?(([0]?\d|1[012])(月(份)?|\.|-|/)?)?(([012]?\d|3[01])(日|号)?)?)$'

        # 英文日月年或月年：匹配'12th SEPTEMBER 2015', 'SEPTEMBER 2015', '18 December 2022'
        dmy_en_reg = '((' + da_ens + ')?[\s]?(' + mo_ens + ')[\s]?(' + '\d{4})' + ')'
        # 英文年月日或年月：匹配'2015 SEPTEMBER 12th'，
        ymd_en_reg = '(' + '(\d{4})[\s]?(' + mo_ens + ')[\s]?(' + da_ens + ')?)'

        # 规格化处理
        normalized_time_str = ''
        standard_res = re.search(standard_reg, strs, re.IGNORECASE)
        dmy_en_res = re.search(dmy_en_reg, strs)
        ymd_en_res = re.search(ymd_en_reg, strs)

        if standard_res: # 标准年月日
            normalized_time_str = _std_time_normalize(strs)
        else:
            if dmy_en_res: # 英文日月年
                res = re.findall(dmy_en_reg, strs, re.IGNORECASE)
                if res:
                    res = res[0][1:]
                    _day = day_dict.get(res[0], '') if res[0] else ''
                    _month = month_dict.get(res[1], '') if res[1] else ''
                    _year = re.findall(r'\d{4}', strs)[0]
                    en_date = '-'.join(list(filter(bool, [_year, _month, _day])))
                    normalized_time_str = _std_time_normalize(en_date)
                    del _day, _month, _year

            elif ymd_en_res: # 英文年月日
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



    def _chinese_dtime_normalizion(strs: str):
        """ 纯中文殊特日期转归一化处理 """

        def _cn_process(strs: str, to_lunar: bool = False):
            """ 汉字年月日转化 """
            # 纯转化可参考：https://blog.csdn.net/qq_35332332/article/details/123881533

            _year, _month, _day = '', '', ''

            if '月份' in strs:
                strs = strs.replace('月份', '月')
            if '腊月' in strs:
                strs = strs.replace('腊月', '十二月')
            if ('元月' in strs) or ('正月' in strs):
                strs = strs.replace('腊月', '一月').replace('正月', '一月')
            if ('农历' in strs) or ('阴历' in strs) or ('初' in strs):
                strs = strs.replace('农历', '').replace('阴历', '').replace('初', '')

            if ('号' in strs) or ('號' in strs):
                strs = strs.replace('号', '日').replace('號', '日')
            if ('月' in strs) and ('日' not in strs) and (strs.index('月') < len(strs) - 1):
                strs += '日'

            if any([i in strs for i in ['年', '月', '日']]):  # 有年月日等字段
                if all(i in strs for i in ['年', '月', '日']):
                    _year, _month, _day, _ = re.split('[年|月|日]', strs)
                elif all(i in strs for i in ['年', '月']):
                    _year, _month, _ = re.split('[年|月]', strs)
                elif '年' in strs:
                    _year, _ = re.split('年', strs)

                if len(_day) >= 3:
                    _day = _day[0] + _day[2]

                _year = ''.join([year_char2num_map.get(i) for i in _year if i in year_char2num_map]) if _year else ''
                _month = ''.join([year_char2num_map.get(i) for i in _month if i in year_char2num_map]) if _month else ''
                _day = ''.join([year_char2num_map.get(i) for i in _day if i in year_char2num_map]) if _day else ''

                if len(_month) == 3:
                    _month = _month[0] + _month[2]
                if len(_day) == 3:
                    _day = _day[0] + _day[2]

            if to_lunar:  # 农历转阳历
                if all([i.isdigit() for i in [_year, _month, _day]]):  # 年月日
                    try:
                        return lunar_date(int(_year), int(_month), int(_day)).to_datetime().strftime('%Y-%m-%d')
                    except:
                        return ''
                elif all([i.isdigit() for i in [_year, _month]]):  # 年月
                    try:
                        return lunar_date(int(_year), int(_month), 1).to_datetime().strftime('%Y-%m')
                    except:
                        return ''
                else:
                    return ''
            else:
                if _year:
                    _year +='年'
                if _month:
                    _month +='月'
                if _day:
                    _day +='日'
                return ''.join(list(filter(bool, [_year, _month, _day])))

        year_char2num_map = {'零': '0', '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4',
                             '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10'}

        # 中文日期规则
        cn_char_reg = '(一|二|三|四|五|六|七|八|九|零|十|〇|○|0)'
        # 阳历中文日期
        ymd_cn_reg = ''.join([
            '(([12]?\d{2,3})|', cn_char_reg, '{4})(\s)?(年)?(上|下)?((半)?年)?',  # 年
            '(', cn_char_reg, '{1,2})?(月(份)?)?'  # 月
                              '(', cn_char_reg, '{1,3})?(日|号)?'  # 日
        ])
        # 农历中文日期
        ymd_lu_reg = ''.join([
            '(((', cn_char_reg, '{4})[\s]?(年))[\s]?',  # 年
            '(((农|阴)?历)?[\s]?((元|正|腊)?月)|', cn_char_reg, '{1,2}(月|大年)?)[\s]?',  # 月
            '((初)?', cn_char_reg, '{1,3}[\s]?(日)?)?[\s]?)'
        ])

        cn_datetime_str = ''
        _lu_datatime_str = re.search(ymd_lu_reg, strs, re.IGNORECASE)
        _cn_datetime_str = re.search(ymd_cn_reg, strs, re.IGNORECASE)

        if any([i in strs for i in ['正月', '元月', '腊月', '初', '大年', '农历', '阴历']]):
            # 农历年月日处理
            if _lu_datatime_str:
                _lu_datatime_str = _lu_datatime_str.group()
                _lu_datatime_str = _cn_process(_lu_datatime_str, to_lunar=True)
                if _lu_datatime_str:
                    cn_datetime_str = _lu_datatime_str

        elif _cn_datetime_str:
            _cn_datetime_str = _cn_datetime_str.group()
            _cn_datetime_str = _cn_process(_cn_datetime_str, to_lunar=False)
            if _cn_datetime_str:
                cn_datetime_str = _cn_datetime_str

        return cn_datetime_str


    def _numeric_dtime_normalizion(strs: str):
        """ 纯数值型殊特时间格式归一化处理(阿拉伯数字日期) """

        def _timestamp_process(strs: str, ymd_timestamp_reg):
            """ 时间戳格式处理"""
            # ymd_timestamp_reg = '(([12]?\d{2,3})(\-|/)?([0]?\d|1[012])(\-|/)?([012]?\d|3[01])(\s)?([0-1]?[0-9]|2[0-3])(\:)([0-5][0-9])(\:)([0-5][0-9]))'
            _datetime_str = re.search(ymd_timestamp_reg, strs)
            _dt_datetime_str = ''
            if _datetime_str:
                _datetime_str = _datetime_str.group()
                try:
                    _dt_datetime_str = datetime.strptime(_datetime_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                except:
                    try:
                        _dt_datetime_str = datetime.strptime(_datetime_str, '%Y-%m-%d%H:%M:%S').strftime('%Y-%m-%d')
                    except:
                        try:
                            _dt_datetime_str = datetime.strptime(_datetime_str, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d')
                        except:
                            pass
                del _datetime_str

            return _dt_datetime_str



        def _specal_num_process(strs: str):
            """ 特殊格式处理 """

            _dt_time_str = ''

            # 17-03-21:
            reg1 = '(((^[012]?\d{1,2}))(-)([0]?\d|1[012])?((-)[012]?\d|3[01])?)$'

            if re.search(reg1, strs):
                _year = strs.split('-')[0]
                _others = "-".join(strs.split('-')[1:])
                if len(_year) == 2:
                    if _year.startswith('0') or _year.startswith('1') or _year.startswith('2'):
                        _year = '20' + _year
                        _dt_time_str = '-'.join([_year, _others])
                    elif _year.startswith('9') or _year.startswith('8') or _year.startswith('7') \
                            or _year.startswith('6') or _year.startswith('5') or _year.startswith('4')\
                            or  _year.startswith('3'):
                        _year = '19' + _year
                        _dt_time_str = '-'.join([_year, _others])

            else:
                # TODO： 未处理，先返回
                _dt_time_str = strs

            return _dt_time_str


        datetime_str = ''
        # 时间戳日期规则及纯数值日期: '2019-06-09 15:00:50' 或 '2019/06/09 15:00:50'
        _num_char_reg1 = r'(([12]?\d{2,3})(\-|/)?([0]?\d|1[012])(\-|/)?([012]?\d|3[01])(\s)?([0-1]?[0-9]|2[0-3])(\:)([0-5][0-9])(\:)([0-5][0-9]))'
        _num_char_reg2 = r'(([12]?\d{2,3})(\s)?(\s|-|/)?([0]?\d|1[012])?(\s)?(\s|-|/)?([012]?\d|3[01])?(\s)?)'

        _num_char_reg = '|'.join([_num_char_reg1, _num_char_reg2])
        _dt_datetime_str = re.search(_num_char_reg, strs, re.IGNORECASE)
        if _dt_datetime_str:
            _dt_datetime_str = _dt_datetime_str.group().replace(" ", "")
            _timestamp_str = _timestamp_process(_dt_datetime_str, _num_char_reg1)
            if _timestamp_str:
                datetime_str = _timestamp_str
            else:
                datetime_str = _specal_num_process(_dt_datetime_str)

        return datetime_str



    def _chinese_numeric_dtime_normalizion(strs: str):
        """ 阿拉伯数字 + 中文 组合日期 归一化"""

        # 1. 06年, '09年4月', 09年度4月4号'
        _dt_time_str = ''
        reg1 = '(^(\d{2})[\s]?(年(度)?)[\s]?(([0]?\d|1[012])(月(份)?))?[\s]?(([012]?\d|3[01])(日|号))?[\s]?)$'

        # 2. '2020年下半年', '2022上半年', 22年上半年', '2022年度下半年'
        reg2 = '(^([12]?\d{2,3})[\s]?((年(度)?)?(上|下)半年)[\s]?)$'
        _dt_match_str2 = re.search(reg2, strs)

        # 3. '1980年代'
        reg3 = '(^([12]?\d{2,3})[\s]?(年代)[\s]?)$'
        _dt_match_str3 = re.search(reg3, strs)

        _dt_match_str = re.search(reg1, strs)
        if _dt_match_str:
            _dt_match_str = _dt_match_str.group().replace(" ", '')

            if ('年度' in _dt_match_str) or ('月份' in _dt_match_str) or ('号' in _dt_match_str):
                _dt_match_str = _dt_match_str.replace('年度', '年').replace('月份', '月').replace('号', '日')

            _year = _dt_match_str.split('年')[0]
            _others = _dt_match_str.split('年')[1]

            if _year.startswith('0') or _year.startswith('1') or _year.startswith('2'):
                _year = '20' + _year
            elif _year.startswith('9') or _year.startswith('8') or _year.startswith('7') \
                    or _year.startswith('6') or _year.startswith('5') or _year.startswith('4') \
                    or _year.startswith('3'):
                _year = '19' + _year

            _dt_time_str = f"{_year}年{_others}" if _others else  f"{_year}年"


        elif _dt_match_str2:
            _dt_match_str2 = _dt_match_str2.group().replace(" ", '')
            _year = re.findall('^([12]?\d{2,3})', _dt_match_str2)[0]
            if _year:
                if _year.startswith('0') or _year.startswith('1') or _year.startswith('2'):
                    _year = '20' + _year
                elif _year.startswith('9') or _year.startswith('8') or _year.startswith('7') \
                        or _year.startswith('6') or _year.startswith('5') or _year.startswith('4') \
                        or _year.startswith('3'):
                    _year = '19' + _year

            _month = ''
            if '上半年' in _dt_match_str2:
                _month = '6月'
            elif '下半年' in _dt_match_str2:
                _month = '12月'

            if _year and _month:
                _dt_time_str = f"{_year}年{_month}"


        elif _dt_match_str3:
            _dt_match_str3 = _dt_match_str3.group().replace(" ", '')
            _year = re.findall('^([12]?\d{2,3})', _dt_match_str3)[0]
            if len(_year) == 4:
                _dt_time_str = f"{_year}年"

        return _dt_time_str



    def _get_time(strs: str):
        # 获取时间表达式

        month_dict, day_dict = _date_unit()
        mo_ens = '|'.join(list(month_dict.keys()))

        # 年月日格式
        # ye_n = '[12]?\d{2,3}'  # 年份数字格式
        ye_n = '(([12]?\d{2,3})|(一|二|三|四|五|六|七|八|九|零|〇|○|0){4}?)'  # 年份数字格式
        mo_n = '([0]?\d|1[012])'  # 月份数字格式
        mo_c = '(元|正|腊|一|二|三|四|五|六|七|八|九|十(一|二)?)'  # 月份汉字格式
        da_n = '([012]?\d|3[01])(th|nd|st|rd)?'  # 日数字格式
        ymd_n = r'(^(?:17|18|19|20)\d{2}' + '(\d{1,2})?' + '(\d{1,2})?)' # 纯数窜字年月日或年月(20221219, 2022)
        ymd_gap = '[\-\~— ～\.\/]{1,2}' # 年跨度格式


        # 组合年月日规则
        ymd_pattern_1 = '(' + ye_n + '[\s]?((上|下)半)?年(初|底|末|度|代|(上|下)半年)?)((' + mo_n + '|' + mo_c + ')月(份|底|初)?)?(' + da_n + '[日号])?' # 带中文格式的年月日
        # ymd_pattern_2 = '^(' + ye_n + ymd_gap + mo_n + '(' + ymd_gap + da_n + ')?)$' # 数值年月日格式或年月格式
        # ymd_pattern_2 = '^(' + ye_n + ymd_gap + mo_n + '(' + ymd_gap + da_n + ')?)$|(' + ymd_n + ')'  # 数值年月日格式或年月格式
        ymd_pattern_2 = '^(' + ye_n + ymd_gap + mo_n + '(' + ymd_gap + da_n + ')?)$'  # 数值年月日格式或年月格式
        # ymd_pattern_2 = '(' + ye_n + '(' + ymd_gap + ')?' + mo_n + '(' + '(' + ymd_gap + ')(' + da_n + ')?))|(' + ye_n + ')'  # 纯数值年月日格式或年月格式
        ymd_pattern_3 = '((' + da_n + '[\s])?(' + mo_ens + ')[\s](' + ye_n + '))$'  # 英文日月年格式，或月年格式
        # ymd_pattern_4 = '((' + ye_n + '[\s]?(Year)?(' +  mo_ens + ')[\s]?)(' + da_n + ')?)$' # 英文年月日格式，或年月格式
        ymd_pattern_4 = '((' + ye_n + '[\s]?(Year)?(' + mo_ens + ')[\s]?)(' + da_n + ')?)'  # 英文年月日格式，或年月格式
        ymd_pattern_5 = '(' + '(([12]?\d|(二)?十(一|二|三|四|五|六|七|八|九)?)世纪)?((\d0|(一|二|三|四|五|六|七|八|九)十)年代)?(初|末)?' + ')$'  # 世纪，年代
        season_pattern = '((春|夏|秋|冬){1,2}(季|天|日)|(第)?(一|二|三|四)(季度)(末)?)'

        # 各类型时间规则汇总
        reg = r'(' + '|'.join([ymd_pattern_1, ymd_pattern_2, ymd_pattern_3, ymd_pattern_4, ymd_pattern_5, ymd_n,
                               season_pattern  ]) + ')'

        # 特殊格式预处理
        is_norm = False
        # 1. 纯中文日期或农历日期，如 '二〇二二年十二月三十一日'， '二〇二二年十二月初二'， '二零二一年元月'
        # if _lange_classifier(strs=strs, rm_dt=False, is_cn=True)[0]: # 中文判断有误
        if not re.findall(r'\d+', strs):
            # print("纯中文日期 .... ")
            specal_cn_time_strs = _chinese_dtime_normalizion(strs)
            if specal_cn_time_strs:
                is_norm = True
                strs = specal_cn_time_strs

        # 2. 纯数值预处理，
        elif len(re.sub('\W', '', t)) == len("".join(re.findall('\d+', t))):
            # print("纯数字日期处理 ... ", strs)
            specal_num_time_strs = _numeric_dtime_normalizion(strs)
            if specal_num_time_strs:
                is_norm = True
                strs = specal_num_time_strs

        # 3. 数值 + 汉字 日期预处理：如 06年, '09年4月', 09年度4月4号'，'2020年下半年', '2022上半年', 22年上半年', '2022年度下半年'
        # _specal_cn_num_reg1 = '(^(\d{2})[\s]?(年(度)?)[\s]?(([0]?\d|1[012])(月(份)?))?[\s]?(([012]?\d|3[01])(日|号))?[\s]?)$'
        # _specal_cn_num_reg2 = '(^([12]?\d{2,3})[\s]?((年(度)?)?(上|下)半年))$'
        else:
            specal_cn_num_time_strs = _chinese_numeric_dtime_normalizion(strs)
            if specal_cn_num_time_strs:
                strs = specal_cn_num_time_strs


        # # 特殊格式预处理:
        # specal_time_strs = _get_specal_time(strs, is_norm)
        # if specal_time_strs:
        #     strs = specal_time_strs


        time_match = re.search(reg, strs, re.IGNORECASE)

        time_info = ''
        if time_match:
            time_info = time_match.group()


        return time_info


    time_info = _get_time(strs)

    time_str = _normalization(time_info)

    return time_str



ts = [
'2021年6月',
 '2022上半年',
 '2019年2月份',
 '2021-12-27',
 '2021-12',
 '2017.11.14',
 '2017.11',
 '2019/09/10',
 '2019/09',
 '12th SEPTEMBER 2015',
 'SEPTEMBER 2015',
 '2015 SEPTEMBER 12th',
 '二零二一年',
 '二零二一年一月',
 '1980年代',
 '20120101',
 '201201',
 '2018-',
 '2020',
 '2016图迈8月',
 '2016年4月5月',
 '2010春季',
 '2022年壹月',
 '2012年1月1日',
 '20120209-2',
 '2019/9-10月',
 '2020.N0.6',
 '2017 Year',
 '20110115-2',
 '2017.11.12',
 '2017年3月',
 '1851',
 '201411',
 '2015-2020',
 '2004',
 '1980',
 '2018',
 '1921',
 '2014.4.3',
 '2017年',
 '2022年5月20日',
 '2020/2021',
 '1833',
 '2015年3月',
 '2020 年',
 '2022年下半年',
 '1906',
 '2006年',
 '2002年',
 '2016年',
 '2006',
 '1994',
 '2014-2015年',
 '2014.7.18',
 '201309',
 '2018-',
 '2020年2月份',
 '1979',
 '2018年度4月',
 '2019年度',
 '1900',
 '2019年',
 '2017年5月',
 'may 2017',
 '201707',
 '2010年',
 '201205',
 '2016 5 10',
 '1954',
 '2017',
 '1774',
 '2005年',
 '1950',
 '2030',
 '2012',
 '1992年',
 '2021下半年',
 '1935',
 '1916',
 '1907年',
 '2021-12-27',
 '201706',
 '2008',
 '2021年3月16日',
 '2016图迈8月',
 '2014-2015',
 '1985',
 '1872',
 '2020年',
 '1915',
 '2017.8.5',
 '2003',
 '1972',
 '2016年4月5月',
 '2022年3月',
 '1989',
 '1930',
 '2019早春',
 '1819',
 '1926',
 '2015-2018',
 '2019年3月',
 '2018年5月',
 '2012年',
 '1945',
 '2022年壹月',
 '2021.5.20',
 '1883',
 '201907',
 '1902',
 '20120209-2',
 '2016年度',
 '2013年3月',
 '2019/9-10月',
 '1918',
 '1917',
 '1958',
 '2013-',
 '1960',
 '2021年',
 '2011年4月',
 '2016',
 'APRIL 2014',
 '2009-2010年',
 '2014',
 '2012-',
 '1999',
 '2012年8月',
 '2016.4.6',
 '2011.11.24',
 '1919 2003',
 '2017年03月',
 '2025年',
 '2015.9.19',
 '2018年3月',
 'JUNE 2016',
 '2014-15',
 '2016年5月',
 '2008年',
 '1986',
 '06年',
 '2017.11.14',
 'APRIL 2017',
 '2016年3月',
 '2020年度',
 '2021 年',
 '1998',
 '2018下半年',
 '1984',
 '2018.06',
 '1975',
 'APRIL 2011',
 'SEPTEMBER 2015',
 '2021-12-07',
 '201311',
 '2016.1.20',
 '2020年5月份',
 '201306',
 '1970',
 '1830',
 '1889-2014',
 '1911',
 '2015-16',
 '2002',
 '2021/6/27',
 '1740',
 '2022',
 '1973',
 '2009.4.5',
 '2016.9.30',
 '1862',
 '1988',
 '2017.11',
 '1812',
 '2015',
 '2012-2015',
 '1933年',
 'JANUARY 2018',
 '20180509',
 '2017 Year',
 '1903',
 '1873',
 '1884',
 '2013',
 '2017年6月28日',
 '2021',
 '1845',
 'APRIL 2012',
 '2014年',
 '2010',
 '2000',
 '2015.12.18',
 '1865',
 '2009',
 '1942',
 '2014.6',
 '2021年度',
 '1976',
 '1905',
 '1960年代',
 '1939',
 '1941',
 '201307',
 '1992',
 '1940 2020',
 '2009年',
 'JUNE 2014',
 '1966',
 '2019',
 '2005',
 'SEPTEMBER 2017',
 '2001',
 '2013.11',
 '2018 年',
 '201402',
 '2009-',
 '2019-06-09 15:00:50',
 '20110115-2',
 '1961',
 '201003',
 '20110112-2',
 '1895',
 '201608',
 '1929年',
 '2015-',
 '201405',
 '1969',
 '2024',
 '2018年10月',
 '2022年',
 '2013-2014',
 '1912',
 '201610',
 'JANUARY 2019',
 '2007',
 '2014 02',
 '2013 10',
 '1978',
 '1926年',
 '1997',
 '1933',
 '2012 09 12',
 '2011年',
 '09年4月',
 '2014.5.16',
 '1927',
 '2018年',
 '202002',
 '2013年',
 '1901',
 '1956',
 '03年6月',
 '2019年2月份',
 '2017年7月',
 '1807',
 'JANUARY 2020',
 '2022年度',
 '1971',
 '2015.2.12',
 '1920',
 '201308',
 '1982',
 '2016年7月',
 '2020-12-27',
 '2005-2006',
 '2015年',
 '1850',
 '2018年7月',
 '201303',
 '2011',
 '1959',
 '2019-2022',
 '1930年代',
 '1903年',
 '2021年上半年',
 '1923年',
 '2020',
 '1949',
 '1987',
 '17-03-21',
  ]

for t in ts:
	out = gettime(t)
	print(f"Input: {t},   转化结果=>>>  {out}")