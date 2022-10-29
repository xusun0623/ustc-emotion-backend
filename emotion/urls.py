from django.contrib import admin
from django.urls import path
import Comment.views as CommentView
import User.views as UserView
import Emoji.views as EmojiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login', UserView.Login.as_view()),
    path('user/add_user', UserView.AddUser.as_view()),
    path('user/delete_user', UserView.DeleteUser.as_view()),
    path('user/edit_info', UserView.EditInfo.as_view()),
    path('user/get_info', UserView.GetInfo.as_view()),
    path('user/get_all_user', UserView.GetAllUser.as_view()),
    path('user/edit_avatar', UserView.EditAvatar.as_view()),
    path('comment/get_uploadparam', CommentView.GetUploadParam.as_view()),
    path('comment/get_comment', CommentView.GetComment.as_view()),
    path('comment/send_comment', CommentView.SendComment.as_view()),
    path('comment/delete_comment', CommentView.DeleteComment.as_view()),
    path('comment/force_refresh', CommentView.ForceRefresh.as_view()),
    path('emoji/set_status', EmojiView.SetStatus.as_view()),
    path('emoji/get_status', EmojiView.GetStatus.as_view()),
    path('emoji/export_excel', EmojiView.ExportExcel.as_view()),
    path('user/test', UserView.Test.as_view()),
]
