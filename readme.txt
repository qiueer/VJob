### 创建数据库及授权
create database db_jobtask default characters set utf8;
create user django identified by 'dj123456'; 
grant all privileges on db_jobtask.* to django@'%';
flush privileges;

### 

### model
model类名不区分在代码里面区分大小写，但是体现在DB里面是不区分的，都是小写
数据库的表名，由appname_modelname构成，appname是什么，在表名中也是什么，但modelname都会被转化为小写


########### setting.py 的配置 BEGIN ###########
### 使用redis作为cache
### 参考文档： http://django-redis-chs.readthedocs.io/zh_CN/latest/
### 需要先安装django_redis : pip install django_redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.253.130:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}, ## 连接池
            #"PASSWORD": "mysecret",   ## 密码
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",    ## 压缩
            #"COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",  ## 压缩算法二，lzma
            "IGNORE_EXCEPTIONS": True,  ## 忽略异常
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds，socket 建立连接超时设置
            "SOCKET_TIMEOUT": 5,  # in seconds， 连接建立后的读写操作超时设置
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.253.130:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",    ## 压缩
            #"COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",  ## 压缩算法二，lzma
            "IGNORE_EXCEPTIONS": True,  ## 忽略异常
        }
    }
}

### 将session写入到redis中 
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

######## setting.py 中的配置 END ###########


### 管理员
1）创建管理员
python manage.py createsuperuser
用户名/密码： admin / qjq@2016


### 新建APP的步骤
1）python manage.py startapp  app
2）setting.py中配置app
3）定义model
4）迁移
python manage.py makemigrations app
python manage.py migrate app


###
python manage.py shell
from django.contrib.auth.models import User
user = User.objects.create_user('qiueer', 'qiueer@qq.com', 'qiueer222220')
user.save()
user.username
user.password