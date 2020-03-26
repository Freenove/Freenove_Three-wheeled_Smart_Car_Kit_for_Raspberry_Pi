# -*- coding: utf-8 -*-
########################################################################
# Filename    : Freenove_Math.py
# Description : These are the global functions.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################
def min(a, b):
    if a<b :
        return a
    else :
        return b

def constrain(x, a, b):
    if x < a :
        return a
    elif x > b:
        return b
    else :
        return x
