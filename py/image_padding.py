#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ Date    : 2022/10/5 13:55
# @ Author  : paperClub
# @ Email   : paperclub@163.com
# @ Site    :



""" 图片padding """

import cv2

def pad(image,
        min_height,
        min_width,
        _bg_color=(255, 255, 255)
        ):
    """ padding """

    h, w, _ = image.shape
    if h < min_height:
        h_pad_top = int((min_height - h) / 2.0)
        h_pad_bottom = int(min_height - h - h_pad_top)
    else:
        h_pad_top = 0
        h_pad_bottom = 0
    if w < min_width:
        w_pad_left = int((min_width - w) / 2.0)
        w_pad_right = int(min_width - w - w_pad_left)
    else:
        w_pad_left = 0
        w_pad_right = 0

    del min_width, min_height, h, w

    return cv2.copyMakeBorder(image, h_pad_top, h_pad_bottom,
                              w_pad_left, w_pad_right,
                              cv2.BORDER_CONSTANT, value=_bg_color)


def scale(image, limt_h, limt_w):
    """image scaling """
    h, w, _ = image.shape
    ratio = min(limt_h / h, limt_w / w) # or  max(limt_h / h, limt_w / w)
    img_pad = cv2.resize(image, (int(w * ratio), int(h * ratio)), cv2.INTER_AREA)
    del image, limt_h, limt_w, ratio,  h, w,

    return img_pad



src = cv2.imread("../src/demo.png")
h = 200
w = 300

img_pad = pad(scale(src, h, w), h, w)

cv2.imshow('ori', src)
cv2.imshow("pad", img_pad)
cv2.waitKey()