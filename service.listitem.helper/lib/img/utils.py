#!/usr/bin/python
# coding: utf-8

########################

# Disable image function for TVOS if ImportError
try:
    from lib.img.image import *
    PIL_supported = True
except ImportError:
    PIL_supported = False

########################

def blurimg(params):
    if PIL_supported:
        param_file = remove_quotes(params.get('file'))
        if param_file:
            try:
                image_blur(params.get('prop','output'),param_file,params.get('radius'))
            except:
                pass
