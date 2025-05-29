"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

def api_root(request):
    """API根端点，提供API信息"""
    return JsonResponse({
        'message': '欢迎使用后端API',
        'version': getattr(settings, 'API_VERSION', 'v1'),
        'app_name': getattr(settings, 'APP_NAME', '后端管理系统'),
        'app_version': getattr(settings, 'APP_VERSION', '1.0.0'),
        'endpoints': {
            'users': '/api/v1/users/',
            'auth': '/api/v1/auth/',
            'core': '/api/v1/core/',
            'ai': '/api/v1/ai/',
            'metaverse': '/api/v1/metaverse/',
            'social': '/api/v1/social/',
            'docs': '/api/docs/',
            'redoc': '/api/redoc/',
            'schema': '/api/schema/',
            'health': '/api/v1/core/system/health/',
        },
        'admin': '/admin/',
        'features': [
            '用户管理系统',
            '身份认证模块',
            'AI功能集成',
            '元宇宙体验',
            '社交互动功能',
            '核心系统功能'
        ]
    })

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),

    # API根端点
    path('api/', api_root, name='api-root'),

    # API版本1
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/core/', include('apps.core.urls')),
    path('api/v1/ai/', include('apps.ai.urls')),
    path('api/v1/metaverse/', include('apps.metaverse.urls')),
    path('api/v1/social/', include('apps.social.urls')),

    # API文档
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# 开发环境下的静态文件和媒体文件处理
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # 开发工具
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass

# 自定义错误页面处理
handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
