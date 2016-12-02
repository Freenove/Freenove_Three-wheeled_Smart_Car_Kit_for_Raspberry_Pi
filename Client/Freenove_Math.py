# -*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  Freenove_Math.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   These are the global functions.
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""
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
