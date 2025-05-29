# 这将确保应用程序总是在Django启动时导入，以便shared_task可以使用此应用程序
from .celery import app as celery_app

__all__ = ('celery_app',)
