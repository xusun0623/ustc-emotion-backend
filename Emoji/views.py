import datetime
from io import BytesIO
from operator import le
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from utils.filter import mid_req
from utils.jwt import decode_jwt_token, vaild_token
from utils.vaild import vaild_int, vaild_datetime

import xlwt

from .models import Status



class ExportExcel(View):
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="teacher"):
                # 仅老师可以导出表情包统计数据
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                
                if(not vaild_datetime(start_time) or not vaild_datetime(end_time)):
                    return mid_req("时间格式不合法", code=0)
                
                return mid_req("获取下载链接成功", {
                    "download_url": "/emoji/export_excel?token={}&start_time={}&end_time={}".format(
                        token,
                        start_time,
                        end_time
                    )
                })

            return mid_req("仅老师可以导出Excel")
        return mid_req("token无效",code=0)

    def get(self, request):
        token = request.GET.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="teacher"):
                # 仅老师可以导出表情包统计数据
                start_time = request.GET.get('start_time')
                end_time = request.GET.get('end_time')
                
                if(not vaild_datetime(start_time) or not vaild_datetime(end_time)):
                    return mid_req("时间格式不合法", code=0)

                status = Status.objects.filter(start_time__gte=start_time, start_time__lte=end_time)
                status_lists = []
                for i in status:
                    status_lists.append({
                        "user_id": i.user_id,
                        "status_type": i.status_type,
                        "start_time": i.start_time,
                        "end_time": i.end_time,
                    })
                
                if(len(status_lists) == 0):
                    return mid_req("没有数据", code=0)
                
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment;filename=device_data.xls'
                ws = xlwt.Workbook(encoding='utf-8')
                w = ws.add_sheet('学生状态数据')
                w.write(0, 0, u'用户ID')
                w.write(0, 1, u'状态')
                w.write(0, 2, u'开始时间')
                w.write(0, 3, u'结束时间')
                excel_row = 1
                for obj in status_lists:
                    w.write(excel_row, 0, obj["user_id"])
                    w.write(excel_row, 1, obj["status_type"])
                    w.write(excel_row, 2, obj["start_time"].strftime("%Y-%m-%d %H:%M") if obj["start_time"] else "")
                    w.write(excel_row, 3, obj["end_time"].strftime("%Y-%m-%d %H:%M") if obj["end_time"] else "")
                    excel_row += 1
                # 写出到IO
                output = BytesIO()
                ws.save(output)
                # 重新定位到开始
                output.seek(0)
                response.write(output.getvalue())
                return response
            return mid_req("仅老师可以导出Excel")
        return mid_req("token无效",code=0)

# Create your views here.
class SetStatus(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="admin" or ret["data"]["roledata"]=="teacher"):
                return mid_req("仅学生可以设置状态")

            if(not vaild_int(request.POST.get('type'), [1,2,3,4,5,6])):
                return mid_req("状态类型type不合法", code =0)

            # 更新此前所有的状态
            previous_status = Status.objects.filter(user_id=ret["data"]["user_id"], end_time=None)
            if(len(previous_status) != 0):
                previous_status.all().update(end_time=datetime.datetime.now())

            new_status = Status(
                user_id = ret["data"]["user_id"],
                status_type = request.POST.get('type'),
                start_time = datetime.datetime.now(),
            )
            new_status.save()
            return mid_req(ret)
        return mid_req("token无效",code=0)

class GetStatus(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="teacher"):
                # 仅老师可以获得表情包统计数据
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                
                if(not vaild_datetime(start_time) or not vaild_datetime(end_time)):
                    return mid_req("时间格式不合法", code=0)

                status = Status.objects.filter(start_time__gte=start_time, start_time__lte=end_time)
                status_lists = []
                for i in status:
                    status_lists.append({
                        "user_id": i.user_id,
                        "status_type": i.status_type,
                        "start_time": i.start_time,
                        "end_time": i.end_time,
                    })
                
                if(len(status_lists) == 0):
                    return mid_req("没有数据", code=0)
                
                # 对表情包数据进行统计
                emoji_num = [0,0,0,0,0,0]
                for i in status_lists:
                    emoji_num[i["status_type"]-1] += 1

                total_num = sum(emoji_num)
                avg_score = (1*emoji_num[0]+2*emoji_num[1]+3*emoji_num[2]+4*emoji_num[3]+5*emoji_num[4]+6*emoji_num[5])/total_num
                var_score = ((1-avg_score)**2*emoji_num[0]+(2-avg_score)**2*emoji_num[1]+(3-avg_score)**2*emoji_num[2]+(4-avg_score)**2*emoji_num[3]+(5-avg_score)**2*emoji_num[4]+(6-avg_score)**2*emoji_num[5])/total_num


                return mid_req("操作成功", {
                    "emoji_num": emoji_num, 
                    "total_num": total_num, 
                    "avg_score": round(avg_score, 2), 
                    "var_score": round(var_score, 2)
                })
            return mid_req("你的权限不够")
        return mid_req("token无效",code=0)