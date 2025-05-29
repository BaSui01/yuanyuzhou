"""
核心权限类
定义系统通用的权限检查逻辑
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限类：只有对象的所有者才能编辑它
    其他用户只能读取
    """
    
    def has_object_permission(self, request, view, obj):
        # 读取权限对任何请求都允许，
        # 所以我们对安全方法SAFE_METHODS总是允许GET，HEAD或OPTIONS请求
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写入权限只给对象的所有者
        return obj.owner == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    允许已认证用户进行任何操作，未认证用户只能读取
    """
    
    def has_permission(self, request, view):
        # 读取权限对任何请求都允许
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写入权限只给已认证用户
        return request.user and request.user.is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    只有管理员可以修改，其他用户只能读取
    """
    
    def has_permission(self, request, view):
        # 读取权限对任何请求都允许
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写入权限只给管理员
        return request.user and request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    只有对象的所有者才能访问
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelfOrAdmin(permissions.BasePermission):
    """
    只有用户自己或管理员才能访问
    """
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
