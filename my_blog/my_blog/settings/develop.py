import os

from .base import *
from my_blog.conf.dev_conf import *

# -*-coding:utf-8-*-
'''
    
'''



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0&torcw4dv^_npr@-t#437txg=ml%&x%07ml!d^9#co5obd-(l'

# 这使用直写式缓存——每次写入缓存的数据也会被写入到数据库。如果数据不在缓存中，会话仅使用数据库进行读取。
# 为了持久化缓存数据，设置 SESSION_ENGINE 为 "django.contrib.sessions.backends.cached_db"
# 在大部分情况下，cached_db 后端将足够快，但如果你需要最后一点的性能，并且愿意不时地删除会话数据，那么 cache 后端适合你。
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# 只允许主机访问
ALLOWED_HOSTS = ['*',]

DEBUG = True


INSTALLED_APPS += [

]

# django.db.utils.InternalError: Packet sequence number wrong - got 1 expected django使用异步报错解决方案
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# 在服务器上运行 collectstatic，将所有的静态文件拷贝至 STATIC_ROOT。
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
# 各个app共用的文件可以放在这
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# 媒体文件地址
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
CKEDITOR_UPLOAD_PATH = "" # 配置ckeditor自定义的存储位置，可以是CDN的地址，如果使用django自身的方式，这里就什么都不写


# SMTP服务器，改为你的邮箱的smtp!
EMAIL_HOST = 'smtp.163.com'
# 改为你自己的邮箱名！
EMAIL_HOST_USER = 'OldKangMe@163.com'
# 你的邮箱密码
# EMAIL_HOST_PASSWORD = 'aT?bWY$F3@3;q8!'
EMAIL_HOST_PASSWORD = 'LWODYUWEZFVPJXRV'
# 发送邮件的端口
EMAIL_PORT = 25
# 是否使用 TLS
EMAIL_USE_TLS = True
# 默认的发件人
DEFAULT_FROM_EMAIL = 'CheckList Site SysManager <OldKangMe@163.com>'



# 使用ck的工具栏并修改，宽度自适应
CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '450px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 预览、表情
            ['Preview', 'Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 格式、字体、大小
            ['Format', 'Font', 'FontSize'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['Image', 'NumberedList', 'BulletedList'],
            # 居左，居中，居右
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            # 最大化
            ['Maximize']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        # 加入代码块插件
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            'codesnippet', 'image2', 'filebrowser', 'widget', 'lineutils', 'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath']),
    },
    # 评论
    'comment': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '280px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 预览、表情
            ['Preview', 'Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 格式、字体、大小
            ['Format', 'Font', 'FontSize'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['Image', 'NumberedList', 'BulletedList'],
            # 居左，居中，居右
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            # 最大化
            ['Maximize']
        ],
        # 加入代码块插件
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            'codesnippet', 'image2', 'filebrowser', 'widget', 'lineutils', 'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath']),
    }
}

AUTHENTICATION_BACKENDS = (
    # Django 后台可独立于 allauth 登录
    'django.contrib.auth.backends.ModelBackend',

    # 配置 allauth 独有的认证方法，如 email 登录
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 设置站点
SITE_ID = 1

# 登录成功后重定向地址
LOGIN_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'WARNING',
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 30,
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}
