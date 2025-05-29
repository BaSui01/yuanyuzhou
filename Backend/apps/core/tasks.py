"""
Celery任务：密钥轮换相关后台任务
"""

import logging
from celery import shared_task
from django.conf import settings
from pathlib import Path
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from key_rotation_manager import KeyRotationManager

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='rotate_encryption_keys')
def rotate_encryption_keys(self, key_names=None, force_rotation=False):
    """
    后台密钥轮换任务

    Args:
        key_names (list): 要轮换的密钥名称列表，None表示轮换所有密钥
        force_rotation (bool): 是否强制轮换，忽略时间间隔检查

    Returns:
        dict: 任务执行结果
    """
    try:
        logger.info(f"开始执行密钥轮换任务 - Task ID: {self.request.id}")

        # 获取项目根目录
        base_dir = Path(settings.BASE_DIR)
        env_file = base_dir / '.env'
        backup_dir = base_dir / 'key_backups'

        # 创建密钥管理器实例
        manager = KeyRotationManager(
            env_file=str(env_file),
            backup_dir=str(backup_dir)
        )

        # 执行密钥轮换
        success = manager.rotate_keys(
            key_names=key_names,
            force=force_rotation
        )

        if success:
            logger.info("密钥轮换任务执行成功")
            return {
                'status': 'success',
                'message': '密钥轮换完成',
                'rotated_keys': key_names or list(manager.key_configs.keys()),
                'task_id': self.request.id
            }
        else:
            logger.error("密钥轮换任务执行失败")
            return {
                'status': 'error',
                'message': '密钥轮换失败',
                'task_id': self.request.id
            }

    except Exception as e:
        logger.error(f"密钥轮换任务异常: {e}")
        return {
            'status': 'error',
            'message': f'任务执行异常: {str(e)}',
            'task_id': self.request.id
        }


@shared_task(name='validate_encryption_keys')
def validate_encryption_keys():
    """
    验证密钥有效性任务

    Returns:
        dict: 验证结果
    """
    try:
        logger.info("开始执行密钥验证任务")

        # 获取项目根目录
        base_dir = Path(settings.BASE_DIR)
        env_file = base_dir / '.env'
        backup_dir = base_dir / 'key_backups'

        # 创建密钥管理器实例
        manager = KeyRotationManager(
            env_file=str(env_file),
            backup_dir=str(backup_dir)
        )

        # 验证密钥
        validation_results = manager.validate_keys()
        all_valid = all(validation_results.values())

        invalid_keys = [k for k, v in validation_results.items() if not v]

        logger.info(f"密钥验证完成 - 有效: {all_valid}, 无效密钥: {invalid_keys}")

        return {
            'status': 'success',
            'all_valid': all_valid,
            'validation_results': validation_results,
            'invalid_keys': invalid_keys,
            'total_keys': len(validation_results),
            'valid_count': sum(validation_results.values())
        }

    except Exception as e:
        logger.error(f"密钥验证任务异常: {e}")
        return {
            'status': 'error',
            'message': f'验证任务异常: {str(e)}'
        }


@shared_task(name='cleanup_key_backups')
def cleanup_key_backups(keep_count=None):
    """
    清理旧密钥备份任务

    Args:
        keep_count (int): 保留的备份数量，None使用配置值

    Returns:
        dict: 清理结果
    """
    try:
        logger.info("开始执行备份清理任务")

        # 获取项目根目录
        base_dir = Path(settings.BASE_DIR)
        env_file = base_dir / '.env'
        backup_dir = base_dir / 'key_backups'

        # 创建密钥管理器实例
        manager = KeyRotationManager(
            env_file=str(env_file),
            backup_dir=str(backup_dir)
        )

        # 获取清理前的备份数量
        backups_before = len(manager.list_backups())

        # 执行清理
        manager._cleanup_old_backups(keep_count)

        # 获取清理后的备份数量
        backups_after = len(manager.list_backups())
        cleaned_count = backups_before - backups_after

        logger.info(f"备份清理完成 - 清理了 {cleaned_count} 个备份文件")

        return {
            'status': 'success',
            'backups_before': backups_before,
            'backups_after': backups_after,
            'cleaned_count': cleaned_count
        }

    except Exception as e:
        logger.error(f"备份清理任务异常: {e}")
        return {
            'status': 'error',
            'message': f'清理任务异常: {str(e)}'
        }


@shared_task(name='check_key_rotation_schedule')
def check_key_rotation_schedule():
    """
    检查密钥轮换计划任务
    如果满足轮换条件，自动触发轮换

    Returns:
        dict: 检查结果
    """
    try:
        logger.info("开始检查密钥轮换计划")

        # 获取项目根目录
        base_dir = Path(settings.BASE_DIR)
        env_file = base_dir / '.env'
        backup_dir = base_dir / 'key_backups'

        # 创建密钥管理器实例
        manager = KeyRotationManager(
            env_file=str(env_file),
            backup_dir=str(backup_dir)
        )

        # 检查是否需要轮换
        should_rotate = manager._should_rotate()

        if should_rotate:
            logger.info("满足轮换条件，触发自动密钥轮换")

            # 异步执行轮换任务
            rotation_task = rotate_encryption_keys.delay()

            return {
                'status': 'success',
                'action': 'rotation_triggered',
                'rotation_task_id': rotation_task.id,
                'message': '已触发自动密钥轮换'
            }
        else:
            logger.info("未到轮换时间，跳过轮换")

            return {
                'status': 'success',
                'action': 'no_rotation_needed',
                'message': '未到轮换时间'
            }

    except Exception as e:
        logger.error(f"轮换计划检查任务异常: {e}")
        return {
            'status': 'error',
            'message': f'计划检查异常: {str(e)}'
        }


@shared_task(name='generate_key_rotation_report')
def generate_key_rotation_report():
    """
    生成密钥轮换报告任务

    Returns:
        dict: 报告数据
    """
    try:
        logger.info("开始生成密钥轮换报告")

        # 获取项目根目录
        base_dir = Path(settings.BASE_DIR)
        env_file = base_dir / '.env'
        backup_dir = base_dir / 'key_backups'

        # 创建密钥管理器实例
        manager = KeyRotationManager(
            env_file=str(env_file),
            backup_dir=str(backup_dir)
        )

        # 收集报告数据
        validation_results = manager.validate_keys()
        backups = manager.list_backups()

        # 读取轮换历史
        import json
        history_file = base_dir / 'key_update_history.json'
        rotation_history = []

        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    rotation_history = json.load(f)
            except json.JSONDecodeError:
                logger.warning("无法读取轮换历史文件")

        # 统计数据
        total_keys = len(validation_results)
        valid_keys = sum(validation_results.values())
        invalid_keys = total_keys - valid_keys
        critical_keys = [k for k, config in manager.key_configs.items() if config.critical]

        # 最近轮换信息
        last_rotation = None
        if rotation_history:
            last_rotation = rotation_history[-1]

        report = {
            'status': 'success',
            'generated_at': manager.current_config.get('timestamp', 'unknown'),
            'key_summary': {
                'total_keys': total_keys,
                'valid_keys': valid_keys,
                'invalid_keys': invalid_keys,
                'critical_keys_count': len(critical_keys),
                'critical_keys': critical_keys
            },
            'validation_results': validation_results,
            'backup_info': {
                'total_backups': len(backups),
                'latest_backup': backups[0] if backups else None,
                'backup_directory': str(backup_dir)
            },
            'rotation_history': {
                'total_rotations': len(rotation_history),
                'last_rotation': last_rotation,
                'recent_rotations': rotation_history[-5:] if rotation_history else []
            },
            'configuration': {
                'rotation_enabled': manager.current_config.get('KEY_ROTATION_ENABLED', 'False'),
                'rotation_interval': manager.current_config.get('KEY_ROTATION_INTERVAL', '24'),
                'backup_count': manager.current_config.get('KEY_BACKUP_COUNT', '3')
            }
        }

        logger.info("密钥轮换报告生成完成")
        return report

    except Exception as e:
        logger.error(f"报告生成任务异常: {e}")
        return {
            'status': 'error',
            'message': f'报告生成异常: {str(e)}'
        }
