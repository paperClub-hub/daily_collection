#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-10-24 8:59
# @Author   : paperclub
# @Desc     : paperclub@163.com


import numpy as np

""" 多维数组排序"""

def get_sorted_top_k_d2(array, top_k=1, axis=-1, reverse=True):
    """
    多维数组排序（支持1维）
    Args:
        array: 多维数组
        top_k: 取数
        axis: 轴维度
        reverse: 是否倒序

    Returns:
        top_sorted_values: 排序后值
        top_sorted_indexes: 值对应位置
    """
    axis_length = array.shape[axis]
    if top_k > axis_length:
        print(f"top_k: {top_k} 超界, 将被设置为：{axis_length}")
        top_k = axis_length

    if reverse:
        # axis_length = array.shape[axis]
        partition_index = np.take(np.argpartition(array, kth=-top_k, axis=axis),
                                  range(axis_length - top_k, axis_length), axis)
    else:
        partition_index = np.take(np.argpartition(array, kth=top_k, axis=axis), range(0, top_k), axis)
    top_values = np.take_along_axis(array, partition_index, axis)
    # 分区后重新排序
    sorted_index = np.argsort(top_values, axis=axis)
    if reverse:
        sorted_index = np.flip(sorted_index, axis=axis)
    top_sorted_values = np.take_along_axis(top_values, sorted_index, axis)
    top_sorted_indexes = np.take_along_axis(partition_index, sorted_index, axis)
    return top_sorted_values, top_sorted_indexes



arr = np.array([[4,3,6], [8,1,4], [0,5,3]])
get_sorted_top_k_d2(arr)
"""结果： 
(array([[6],
        [8],
        [5]]),
array([[2],
        [0],
        [1]]))
"""