#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-11-21 13:35
# @Author   : paperclub
# @Desc     : paperclub@163.com



""" 检测目录下文件大小， 打印大于指定大小的文件地址"""
import os
from os.path import join, getsize

def check_size(work_dir: str, limt_size:int = 100):

	for root, dirs, files in os.walk(work_dir, topdown=False):
		for name in files:
			file_path = join(root, name)
			file_size = (getsize(file_path) / (1024*1024)) # M
			if file_size >= limt_size:
				print(f"【+】超过指定大小{limt_size}: {file_size}, {file_path} ")


root = "./"
check_size(root)