import re
from django.shortcuts import render
from django.views import View
import datetime

from .models import CommentModel as Comment
from User.models import Admin, Teacher, Student

from utils.filter import mid_req
from utils.jwt import decode_jwt_token, vaild_token
from utils.vaild import vaild_int, vaild_re
from utils.oss import getUploadParam
from toxic import illegal_check

tmp_list = []

def getTmpList():
    global tmp_list
    return tmp_list

def setTmpList(l):
    global tmp_list
    tmp_list = l

# 强制从数据库中获取数据
def forceRefresh():
    global tmp_list
    tmp_list = []
    commentList = Comment.objects.order_by("-time").filter(is_delete=0)[0:100]
    for comment in commentList:
        tmp_list.append({
            "comment_id": comment.id,
            "user_id": comment.user_id,
            "user_type": comment.user_type,
            "nick_name": comment.nick_name,
            "user_avatar": comment.user_avatar,
            "cont": comment.cont,
            "comment_type": comment.comment_type,
            "time": comment.time,
            "is_delete": comment.is_delete,
            "toxic_type": comment.toxic_type,
        })
    return tmp_list

class GetUploadParam(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            return mid_req("获取上传参数成功", getUploadParam())
        return mid_req("token无效",code=0)

class DeleteComment(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            # 用户类型为admin或teacher，可以直接删除comment_id对应的评论
            comment_id = request.POST.get('comment_id')
            if(comment_id and vaild_int(comment_id)):
                if(ret["data"]["roledata"]=="admin" or ret["data"]["roledata"]=="teacher"):
                    comment = Comment.objects.filter(id=comment_id)
                    if(len(comment)==0):
                        return mid_req("评论不存在")
                    comment = comment[0]
                    if(comment.is_delete==1):
                        return mid_req("该评论已被删除",code=0)
                    comment.is_delete = 1
                    comment.save()
                    forceRefresh()
                    return mid_req("删除成功")
                # 用户类型为student，可以删除comment_id对应的评论
                elif(ret["data"]["roledata"]=="student"):
                    comment = Comment.objects.filter(id=comment_id)
                    if(len(comment)==0):
                        return mid_req("评论不存在")
                    comment = comment[0]
                    stu_info = Student.objects.filter(id=comment.user_id)
                    if(len(stu_info)==0):
                        return mid_req("你不能删除管理员或老师的评论")
                    stu_info = stu_info[0]
                    if(stu_info.username == ret["data"]["username"]):
                        if(comment.is_delete==1):
                            return mid_req("该评论已被删除",code=0)
                        comment.is_delete = 1
                        comment.save()
                        forceRefresh()
                        return mid_req("删除成功")
                    return mid_req("你不能删除别人的评论")
            return mid_req("comment_id错误", code=0)
        return mid_req("token无效",code=0)

class ForceRefresh(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            forceRefresh()
            return mid_req("刷新成功",code=0)
        return mid_req("token无效",code=0)

class SendComment(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            usr = {
                "admin": Admin,
                "teacher": Teacher,
                "student": Student,
            }[ret["data"]["roledata"]].objects.get(username=ret["data"]["username"])

            tmp_cont = request.POST.get('cont')
            tmp_cont_type = request.POST.get('type')
        
            if(not vaild_re(tmp_cont, r'^[\s\S]*.*[^\s][\s\S]*$')):
                return mid_req("评论内容不能为空")
            
            if(tmp_cont_type == None or tmp_cont_type != "image"):
                tmp_cont_type = "text"

            toxic_type_tmp = illegal_check.check(tmp_cont)
            if(tmp_cont_type=="image"):
                toxic_type_tmp = -1

            comment = Comment(
                user_id = usr.id,
                user_type = ret["data"]["roledata"],
                nick_name = usr.nickname,
                user_avatar = usr.avatar,
                cont = tmp_cont,
                comment_type = tmp_cont_type,
                time = datetime.datetime.now(),
                is_delete = 0,
                toxic_type = toxic_type_tmp,
            )
            comment.save()

            tmp_tmp_list = getTmpList()
            tmp_tmp_list.insert(0, { #向头部追加新的数据
                "comment_id": comment.id,
                "user_id": usr.id,
                "user_type": ret["data"]["roledata"],
                "nick_name": usr.nickname,
                "user_avatar": usr.avatar,
                "cont": tmp_cont,
                "comment_type": tmp_cont_type,
                "time": datetime.datetime.now(),
                "is_delete": 0,
                "toxic_type": toxic_type_tmp,
            })
            tmp_tmp_list = tmp_tmp_list[:100] #截断
            setTmpList(tmp_tmp_list)

            return mid_req("发表成功")
        return mid_req("token无效",code=0)

def filterComment(comments, mine_id):
    tmp = []
    for i in comments:
        if (i["user_id"] == mine_id):
            i["is_mine"] = 1
        else:
            i["is_mine"] = 0
        tmp.append(i)
    return tmp

# Create your views here.
class GetComment(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            mine_id = ret["data"]["user_id"]
            if(getTmpList() == []):
                return mid_req("获取成功", filterComment(forceRefresh(), mine_id)) #强制刷新
            return mid_req("获取成功", filterComment(getTmpList(), mine_id))
        return mid_req("token无效",code=0)