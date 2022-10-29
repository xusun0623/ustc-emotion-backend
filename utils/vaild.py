import datetime
import re

def vaild_datetime(str_):
    try:
        datetime.datetime.strptime(str_, '%Y-%m-%d %H:%M')
    except Exception as e:
        return False
    return True

def vaild_int(int_val,range=[]):
    try:
        int(int_val)
    except Exception as e:
        return False
    return True if len(range) == 0 else int(int_val) in range
    

def vaild_re(str_, restr_):
    if(str_ == None):
        return False
    pattern = re.compile(restr_)
    result = pattern.findall(str_)
    if (len(result) == 0):
        return False
    else:
        return True