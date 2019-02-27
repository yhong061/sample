#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#string to hex
#--------------------------------------
print(':'.join(hex(ord(x))[2:] for x in '9ASF51272PZ-2G3B1'))
#'39:41:53:46:35:31:32:37:32:50:5a:2d:32:47:33:42:31'
print(''.join(hex(ord(x))[2:] for x in '9ASF51272PZ-2G3B1'))
#'394153463531323732505a2d3247334231'

