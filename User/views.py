import json
from operator import le
from django.shortcuts import render, HttpResponse
from django.views import View
from utils.jwt import get_jwt_token, decode_jwt_token, vaild_token
import utils.md5 as md5
from utils.filter import mid_req
from .models import Admin, Student, Teacher
from utils.vaild import vaild_re, vaild_int
from utils.oss import getUploadParam
from toxic import illegal_check
from Comment.models import CommentModel 
from Comment.views import forceRefresh 

def changeAvatarNickname():
    print(123)
    forceRefresh()

class Test(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            all_comments = CommentModel.objects.all()
            for single_comment in all_comments:
                single_comment.toxic_type = illegal_check.check(single_comment.cont)
                print(single_comment.toxic_type)
                single_comment.save()
            # ret = decode_jwt_token(token)
            ret = illegal_check.check("草泥马")
            return mid_req(ret)
        return mid_req("ret")


class EditAvatar(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            roledata = ret["data"]["roledata"] # admin teacher student
            roleid = ret["data"]["user_id"] # admin teacher student
            head_url = request.POST.get('url')
            obj_infos = []

            if (roledata == "admin"):
                obj_infos = Admin.objects.filter(id=roleid)
            if (roledata == "teacher"):
                obj_infos = Teacher.objects.filter(id=roleid)
            if (roledata == "student"):
                obj_infos = Student.objects.filter(id=roleid)
            
            if(len(obj_infos) == 0):
                return mid_req("未匹配到用户", code=0)
            obj_info = obj_infos[0]
            if(vaild_re(head_url, r'^([hH][tT]{2}[pP]://|[hH][tT]{2}[pP][sS]://)(([A-Za-z0-9-~]+).)+([A-Za-z0-9-~\\/])+$')):
                obj_info.avatar = head_url
            else:
                return mid_req("头像Url校验不通过", code=0)
            obj_info.save()
            need_update_comments = CommentModel.objects.filter(user_id=roleid, user_type=roledata)
            need_update_comments.update(user_avatar=head_url)
            changeAvatarNickname()

            return mid_req("success")
        return mid_req("token无效",code=0)

class GetAllUser(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="admin"):
                # 操作
                student_list = Student.objects.all()
                ret_list = []
                for student in student_list:
                    ret_list.append({
                        "id": student.id,
                        "username": student.username,
                        "number": student.number,
                        "nickname": student.nickname,
                        "school_class": student.school_class,
                        "major": student.major,
                        "avatar": student.avatar,
                        "age": student.age,
                        "phone": student.phone,
                    })
                return mid_req("获取成功", ret_list)
            return mid_req("你的权限不够")
        return mid_req("token无效",code=0)

class GetInfo(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="admin"):
                # 获取管理员信息
                objs_info = Admin.objects.filter(username=ret["data"]["username"])
                if(len(objs_info)==0):
                    return mid_req("未找到用户信息", code=0)
                obj_info = objs_info[0]
                return mid_req({
                    "admin_id": obj_info.id,
                    "username": obj_info.username,
                    "nickname": obj_info.nickname,
                    "age": obj_info.age,
                    "gender": obj_info.gender,
                    "phone": obj_info.phone,
                })
            if(ret["data"]["roledata"]=="teacher"):
                objs_info = Teacher.objects.filter(username=ret["data"]["username"])
                if(len(objs_info)==0):
                    return mid_req("未找到用户信息", code=0)
                obj_info = objs_info[0]
                # 操作
                return mid_req({
                    "teacher_id": obj_info.id,
                    "username": obj_info.username,
                    "nickname": obj_info.nickname,
                    "age": obj_info.age,
                    "gender": obj_info.gender,
                    "phone": obj_info.phone,
                })
            if(ret["data"]["roledata"]=="student"):
                objs_info = Student.objects.filter(username=ret["data"]["username"])
                if(len(objs_info)==0):
                    return mid_req("未找到用户信息", code=0)
                obj_info = objs_info[0]
                # 操作
                return mid_req({
                    "stu_id": obj_info.id,
                    "username": obj_info.username,
                    "number": obj_info.number,
                    "nickname": obj_info.nickname,
                    "age": obj_info.age,
                    "gender": obj_info.gender,
                    "school_class": obj_info.school_class,
                    "major": obj_info.major,
                    "phone": obj_info.phone,
                })
            return mid_req("你的权限不够")
        return mid_req("token无效",code=0)

class EditInfo(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="admin"):
                # 获取管理员信息
                objs_info = Admin.objects.filter(username=ret["data"]["username"])
                user_type = request.POST.get('type') # 用户类型
                user_id = request.POST.get('user_id') # 用户ID

                if(user_id != None):
                    if(vaild_int(user_id)):
                        user_id = int(user_id)
                    else:
                       user_id = 0

                other_flag = (vaild_int(user_type, [2, 3]) and user_id != 0)

                if(other_flag): #改别人的
                    print("改别人的")
                    user_type = int(user_type)
                    objs_info = [Teacher, Student][user_type - 2].objects.filter(id=user_id)
                else:
                    # 是否需要更新评论的昵称
                    print("改自己的")
                    update_nickname_flag = (objs_info[0].nickname != request.POST.get('nickname'))
                    if(update_nickname_flag):
                        # 更新评论的昵称
                        CommentModel.objects.filter(
                            user_id = ret["data"]["user_id"], 
                            user_type = "admin",
                        ).update(nick_name = request.POST.get('nickname'))
                        changeAvatarNickname()

                if(len(objs_info)==0):
                    return mid_req("未找到用户信息", code=0)

                obj_info = objs_info[0]
                nickname = request.POST.get('nickname') #用户昵称
                password = request.POST.get('password') #用户密码
                avatar = request.POST.get('avatar') #用户头像
                gender = request.POST.get('gender') #性别
                age = request.POST.get('age') #年龄
                phone = request.POST.get('phone') #电话


                if(vaild_int(gender, [0,1])):
                    obj_info.gender = gender
                if(vaild_re(nickname, r'^.{3,20}$')):
                    obj_info.nickname = nickname
                if(vaild_re(age, r'^120$|^[1-9]$|^((1[0-1])|[1-9])\d$')):
                    obj_info.age = age
                if(vaild_re(password, r'^.{3,20}$')):
                    obj_info.password = md5.encode(password)
                if(vaild_re(phone, r'^1[3-9]\d{9}$')):
                    obj_info.phone = phone
                elif(phone != None and phone != ""):
                    return mid_req("手机号格式错误", code=0)
                if(vaild_re(avatar, r'^([hH][tT]{2}[pP]://|[hH][tT]{2}[pP][sS]://)(([A-Za-z0-9-~]+).)+([A-Za-z0-9-~\\/])+$')):
                    obj_info.avatar = avatar
                if(vaild_int(user_type, [2, 3]) and (not other_flag)):
                   return mid_req("管理员不能把自己降为其他身份", code=0)
                elif(vaild_int(user_type, [1, 2, 3]) and other_flag):
                    obj_info.type = user_type
                obj_info.save()
                return mid_req("更新完成")

            if(ret["data"]["roledata"]=="teacher"):
                # 获取管理员信息
                objs_info = Teacher.objects.filter(username=ret["data"]["username"])

                if(len(objs_info)==0):
                    return mid_req("未找到用户信息", code=0)

                obj_info = objs_info[0]
                nickname = request.POST.get('nickname') #用户昵称
                password = request.POST.get('password') #用户密码
                avatar = request.POST.get('avatar') #用户头像
                gender = request.POST.get('gender') #性别
                age = request.POST.get('age') #用户头像
                phone = request.POST.get('phone') #用户头像

                if(vaild_re(nickname, r'^.{3,20}$')):
                    update_nickname_flag = (obj_info.nickname != nickname)
                    if(update_nickname_flag):
                        # 更新评论的昵称
                        CommentModel.objects.filter(
                            user_id = ret["data"]["user_id"], 
                            user_type = "teacher",
                        ).update(nick_name = nickname)
                        changeAvatarNickname()
                    obj_info.nickname = nickname
                if(vaild_re(phone, r'^1[3-9]\d{9}$')):
                    obj_info.phone = phone
                else:
                    return mid_req("手机号格式错误", code=0)
                if(vaild_int(gender, [0,1])):
                    obj_info.gender = gender
                if(vaild_re(age, r'^120$|^[1-9]$|^((1[0-1])|[1-9])\d$')):
                    obj_info.age = age
                else:
                    return mid_req("年龄格式错误", code=0)
                if(vaild_re(password, r'^.{3,20}$')):
                    obj_info.password = md5.encode(password)
                if(vaild_re(avatar, r'^([hH][tT]{2}[pP]://|[hH][tT]{2}[pP][sS]://)(([A-Za-z0-9-~]+).)+([A-Za-z0-9-~\\/])+$')):
                    obj_info.avatar = avatar
                obj_info.save()


                return mid_req("更新完成")

            if(ret["data"]["roledata"]=="student"):
                # 获取管理员信息
                objs_info = Student.objects.filter(username=ret["data"]["username"])

                if(len(objs_info)==0):
                    return mid_req("未找到用户信息", code=0)

                obj_info = objs_info[0]
                number = request.POST.get('number') #学号
                age = request.POST.get('age') #年龄
                gender = request.POST.get('gender') #性别
                school_class = request.POST.get('school_class') #专业
                major = request.POST.get('major') #专业
                nickname = request.POST.get('nickname') #用户昵称
                password = request.POST.get('password') #用户密码
                avatar = request.POST.get('avatar') #用户头像
                phone = request.POST.get('phone') #用户头像

                print(phone)

                if(vaild_re(number, r'^.{3,20}$')):
                    obj_info.number = number
                if(vaild_re(phone, r'^1[3-9]\d{9}$')):
                    obj_info.phone = phone
                elif(phone != None and str(phone) != ""):
                    return mid_req("手机号格式错误", code=0)
                if(vaild_re(age, r'^120$|^[1-9]$|^((1[0-1])|[1-9])\d$')):
                    obj_info.age = age
                if(vaild_int(gender, [0,1])):
                    obj_info.gender = gender
                if(vaild_re(school_class, r'^.{3,20}$')):
                    obj_info.school_class = school_class
                if(vaild_re(major, r'^.{3,20}$')):
                    obj_info.major = major
                if(vaild_re(nickname, r'^.{3,20}$')):
                    update_nickname_flag = (obj_info.nickname != nickname)
                    if(update_nickname_flag):
                        # 更新评论的昵称
                        CommentModel.objects.filter(
                            user_id = ret["data"]["user_id"], 
                            user_type = "student",
                        ).update(nick_name = nickname)
                        changeAvatarNickname()
                    obj_info.nickname = nickname
                if(vaild_re(password, r'^.{3,20}$')):
                    obj_info.password = md5.encode(password)
                if(vaild_re(avatar, r'^([hH][tT]{2}[pP]://|[hH][tT]{2}[pP][sS]://)(([A-Za-z0-9-~]+).)+([A-Za-z0-9-~\\/])+$')):
                    obj_info.avatar = avatar
                obj_info.save()
                return mid_req("更新完成")

            return mid_req("你的权限不够")
        return mid_req("token无效",code=0)

class DeleteUser(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        user_type = request.POST.get('type')
        user_id = request.POST.get('user_id')

        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="admin"):
                # 操作
                if(not vaild_int(user_type,[2,3])):
                    return mid_req("无效的type类型",code=0)
                if(not vaild_int(user_id)):
                    return mid_req("无效的user_id用户ID",code=0)
                user_type = int(user_type)
                filter_objs = [Teacher,Student][user_type-2].objects.filter(id=user_id)
                if(len(filter_objs)==0):
                    return mid_req("没有对应的用户",code=0)
                filter_objs[0].delete()
                return mid_req("删除成功")
            return mid_req("你的权限不够")
        return mid_req("token无效",code=0)

class AddUser(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        token = request.POST.get('token')
        if(vaild_token(token)):
            ret = decode_jwt_token(token)
            if(ret["data"]["roledata"]=="admin"):
                # 管理员身份
                # admin_username = ret["data"]["username"]
                # admin_time = ret["time"]
                # 用户名 & 密码
                username = request.POST.get('username')
                password = request.POST.get('password')
                user_type = request.POST.get('type')

                if(username!=None and password!=None and vaild_re(username, r'^.{3,20}$') and vaild_re(password, r'^.{3,20}$')):
                    if(not vaild_int(user_type,[1,2,3])):
                        return mid_req("参数type不合法", code=0)
                    # 新增用户
                    user_type = int(user_type)
                    filter_user = [Admin, Teacher, Student][user_type-1].objects.filter(username=username)
                    if(len(filter_user)>0):
                        return mid_req("用户名已存在", code=0)
                    new_user = [Admin, Teacher, Student][user_type-1](
                        username=username,
                        password=md5.encode(password)
                    )
                    new_user.save()
                    return mid_req("新增成功")
                else:
                    return mid_req("请确保字段长度为3~20")
            else:
                return mid_req("你的权限不够", code=0)
        else:
            return mid_req("Token解析失败", code=0)

# 用户登录
class Login(View):
    def get(self, request):
        return mid_req("GET方法不被允许")
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if(not vaild_int(request.POST.get('type'),[1,2,3])):
            return mid_req("参数type错误", code=0)

        user_type = int(request.POST.get('type'))
        obj = [Admin,Teacher,Student][user_type-1].objects.filter(username=username)
        if(len(obj)==0):
            return mid_req("用户名不存在", code=0)
        else: #账号存在
            hash_password = md5.encode(password)
            if(hash_password==obj[0].password):
                ret_data = {
                    "token": get_jwt_token(
                        username = username,
                        roledata = ["admin","teacher","student"][user_type-1],
                        user_id = obj[0].id
                    ),
                    "head": obj[0].avatar
                }
                return mid_req("登录成功！", data=ret_data)
            else:
                return mid_req("密码不匹配", code=0)