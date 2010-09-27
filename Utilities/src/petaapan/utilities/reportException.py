# -*- coding: utf-8 -*-
'''
Provides a complete exception report including the traceback
Compatible with Python 2.5 or later

Created on 2010-08-28

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

import sys
import traceback

def report(ex, logger=None):
    if ex is None: return
    # Report information from exception
    st = []
    st.append(['Exception Report\n', '\n'])
    st.append(['Exception Arguments\n'])
    if ex.args and len(ex.args) > 0: st.append(['\tError: %s\n' % ex.args[0]])
    if ex.args and len(ex.args) > 1: st.append(['\tDescription: %s\n' % ex.args[1]]) 
    for arg in ex.args[2:]:
        st.append(['\t' + str(arg) + '\n'])      
        
    # Report system information about exception 
    
    st.append(['System Exception Information:\n'])
    extype, value, tb = sys.exc_info()
    try:
        st.append(traceback.format_exception(extype, value, tb))
    finally:
        del tb
        
    # Log the error if possible
    
    if logger:
        for ln in st:
            logger(ln)
    return st