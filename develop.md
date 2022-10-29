> 禁用 VSCode 中 Markdown 警告下划线：setting -> markdownlint -> setting.json -> "MD047": false   

> ORM无法操作到数据库级别，只能操作到数据表
  
> 参考：https://www.runoob.com/django/django-model.html

### 1. 新建一个模型

```shell
django-admin startapp TestModel
```

```python
# 修改 TestModel/models.py 文件，代码如下
# models.py
from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=20)
```

`在settings.py中，修改INSTALLED_APPS`：

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TestModel',               # 添加此项
)
```

### 2. 迁移&更新此模型

```shell
python3 manage.py makemigrations   # 创建表结构
python3 manage.py migrate   # 更新此模型
```

### 3. 数据库增删改查  

```python
from user.models import Test

# 数据库操作
def add(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")

# 数据库操作
def get(request):
    # 初始化
    response = ""
    response1 = ""
    
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Test.objects.all()
        
    # filter相当于SQL中的WHERE，可设置条件过滤结果
    list = Test.objects.filter(id=1) 
    
    # 获取单个对象
    response3 = Test.objects.get(id=1) 
    
    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    Test.objects.order_by('name')[0:2]
    
    #数据排序
    Test.objects.order_by("id")
    
    # 上面的方法可以连锁使用
    Test.objects.filter(name="runoob").order_by("id")
    
    # 输出所有数据
    for var in list:
        response1 += var.name + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")

# 数据库操作
def update(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = Test.objects.get(id=1)
    test1.name = 'Google'
    test1.save()
    
    # 另外一种方式
    #Test.objects.filter(id=1).update(name='Google')
    
    # 修改所有的列
    # Test.objects.all().update(name='Google')
    
    return HttpResponse("<p>修改成功</p>")

# 数据库操作
def delete(request):
    # 删除id=1的数据
    test1 = Test.objects.get(id=1)
    test1.delete()
    
    # 另外一种方式
    # Test.objects.filter(id=1).delete()
    
    # 删除所有数据
    # Test.objects.all().delete()
    
    return HttpResponse("<p>删除成功</p>")
```

### 4. Jwt加解密

```python
# 加密
from utils.jwt import get_jwt_token
get_jwt_token(username="xusun000", roledata="student", user_id=123)
```  

```python
# 解密
from utils.jwt import decode_jwt_token
decode_jwt_token("****")
```  

### 5. 扫描依赖并注入requirement.txt中  

```shell
pipreqs ./ --encoding=utf-8 --force
```

### 6. 部署到线上并服务  

```shell
pip3 install -r requirement.txt
nohup python3 manage.py runserver 0.0.0.0:8080 > log.txt 2>&1 &

# 查看端口 & kill端口
lsof -i:8080
kill -9 PID
```
