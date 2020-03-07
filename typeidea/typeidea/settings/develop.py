# Author : zmd
# Date : 2019/12/6 17:09
# Desc :

from .base import *


DEBUG=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 之所以在develop.py中增加，因为该工具只能在开发和测试阶段使用
# 并且django-debug-toolbar只有在DEBUG=True时才会生效

INSTALLED_APPS += [
    'debug_toolbar',    # develop设置中引入django-debug-toolbar,用于做性能排查
    'pympler',          # 引入内存占用分析
    # 'debug_toolbar_line_profiler',      # 引入行级性能分析插件
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # django-debug-toolbar中间件
]

INTERNAL_IPS = ['127.0.0.1']

# 配置django-debug-toolbar
DEBUG_TOOLBAR_PANELS = [

    # 默认的panel
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',

    # 第三方panel
    # 'djdt_flamegraph.FlamegraphPanel',  # djdt_flamegraph火焰图，windows中可能不兼容
    'pympler.panels.MemoryPanel',         # 内存占用分析
    # 'debug_toolbar_line_profiler.panel.ProfilingPanel',     # 行级性能分析
]
# 如果上方的debug_toolbar配置展示不出来，可以修改JQUERY_URL为国内的CDN地址
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL':'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
}
