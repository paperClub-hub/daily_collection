
## 说明


#### 1. py/model_convert.py, paddlenlp模型转化为torch模型（包括根据url下载模型的方法等）
#### 2. py/docment_text2sentences.py, 将文本（中文）按照标点符号拆分成单句，并保留原始标点符号
#### 3. py/rule_pattern_demo1.py, 基于规则处理 “室内面积”、“费用”等实体关键字
#### 4. py/zipfiles.py, 基于协程进行文件压缩，压缩后自动删除原始文件
#### 5. py/logging_with_different_color.py, 根据日志登记显示不同的颜色
#### 6. py/check_str_is_en_cn.py, 判断字符串是否全为中文、包含中文，是否全为英文、包含英文
#### 7. py/has_number.py, 判断字符串中是否有【数值性数据】，如“123”，“三”，“Jan”, “one” 等..