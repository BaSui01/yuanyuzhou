"""
Core exceptions for the application.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class BaseAPIException(APIException):
    """Base exception for all API exceptions."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "发生了未知错误。"
    default_code = "error"


class ResourceNotFound(BaseAPIException):
    """Resource not found exception."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "请求的资源不存在。"
    default_code = "not_found"


class PermissionDenied(BaseAPIException):
    """Permission denied exception."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "您没有执行此操作的权限。"
    default_code = "permission_denied"


class ValidationError(BaseAPIException):
    """Validation error exception."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "提供的数据无效。"
    default_code = "validation_error"
