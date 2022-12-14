from django.shortcuts import HttpResponse
import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

def mid_req(msg="操作成功", data="", code=1):
    ret = {
        "msg": msg,
        "data": data,
        "code": code
    }
    return HttpResponse(json.dumps(ret,cls=DateEncoder), content_type='application/json')
