#!/usr/bin/env python3
"""
密钥轮换定时调度器
使用Celery Beat进行定时任务调度
"""

import os
import django
from pathlib import Path

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django.utils import timezone
import json
import logging

logger = logging.getLogger(__name__)


class KeyRotationScheduler:
    """密钥轮换定时调度器"""

    def __init__(self):
        self.task_configs = {
            'key_rotation_check': {
                'task': 'check_key_rotation_schedule',
                'description': '检查密钥轮换计划',
                'default_interval': 1,  # 每小时检查一次
                'interval_type': 'hours'
            },
            'key_validation': {
                'task': 'validate_encryption_keys',
                'description': '验证密钥有效性',
                'default_interval': 6,  # 每6小时验证一次
                'interval_type': 'hours'
            },
            'backup_cleanup': {
                'task': 'cleanup_key_backups',
                'description': '清理旧密钥备份',
                'default_interval': 1,  # 每天清理一次
                'interval_type': 'days'
            },
            'generate_report': {
                'task': 'generate_key_rotation_report',
                'description': '生成密钥轮换报告',
                'default_interval': 7,  # 每周生成一次报告
                'interval_type': 'days'
            }
        }

    def create_or_update_schedule(self, task_name, interval_value=None, interval_type=None, enabled=True):
        """创建或更新定时任务"""
        if task_name not in self.task_configs:
            raise ValueError(f"未知的任务名称: {task_name}")

        config = self.task_configs[task_name]

        # 使用提供的参数或默认值
        interval_value = interval_value or config['default_interval']
        interval_type = interval_type or config['interval_type']

        # 创建或获取间隔调度
        if interval_type == 'hours':
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=interval_value,
                period=IntervalSchedule.HOURS
            )
        elif interval_type == 'days':
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=interval_value,
                period=IntervalSchedule.DAYS
            )
        elif interval_type == 'minutes':
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=interval_value,
                period=IntervalSchedule.MINUTES
            )
        else:
            raise ValueError(f"不支持的间隔类型: {interval_type}")

        # 创建或更新周期任务
        task, created = PeriodicTask.objects.get_or_create(
            name=f"key_rotation_{task_name}",
            defaults={
                'task': config['task'],
                'interval': schedule,
                'enabled': enabled,
                'description': config['description']
            }
        )

        if not created:
            # 更新现有任务
            task.interval = schedule
            task.enabled = enabled
            task.description = config['description']
            task.save()

        action = "创建" if created else "更新"
        logger.info(f"{action}定时任务: {task.name} - 每{interval_value}{interval_type}")

        return task

    def create_cron_schedule(self, task_name, hour=0, minute=0, day_of_week='*', enabled=True):
        """创建基于Cron表达式的定时任务"""
        if task_name not in self.task_configs:
            raise ValueError(f"未知的任务名称: {task_name}")

        config = self.task_configs[task_name]

        # 创建或获取Cron调度
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month='*',
            month_of_year='*'
        )

        # 创建或更新周期任务
        task, created = PeriodicTask.objects.get_or_create(
            name=f"key_rotation_{task_name}_cron",
            defaults={
                'task': config['task'],
                'crontab': schedule,
                'enabled': enabled,
                'description': f"{config['description']} (Cron调度)"
            }
        )

        if not created:
            task.crontab = schedule
            task.enabled = enabled
            task.save()

        action = "创建" if created else "更新"
        logger.info(f"{action}Cron定时任务: {task.name} - {hour}:{minute:02d}")

        return task

    def setup_default_schedules(self):
        """设置默认的定时任务"""
        logger.info("设置默认密钥轮换定时任务...")

        # 检查密钥轮换计划 - 每小时执行
        self.create_or_update_schedule('key_rotation_check', 1, 'hours')

        # 验证密钥有效性 - 每6小时执行
        self.create_or_update_schedule('key_validation', 6, 'hours')

        # 清理旧备份 - 每天凌晨2点执行
        self.create_cron_schedule('backup_cleanup', hour=2, minute=0)

        # 生成报告 - 每周一上午9点执行
        self.create_cron_schedule('generate_report', hour=9, minute=0, day_of_week=1)

        logger.info("默认定时任务设置完成")

    def setup_production_schedules(self):
        """设置生产环境的定时任务"""
        logger.info("设置生产环境密钥轮换定时任务...")

        # 生产环境更频繁的检查
        self.create_or_update_schedule('key_rotation_check', 30, 'minutes')

        # 密钥验证 - 每4小时执行
        self.create_or_update_schedule('key_validation', 4, 'hours')

        # 清理旧备份 - 每天凌晨3点执行
        self.create_cron_schedule('backup_cleanup', hour=3, minute=0)

        # 生成报告 - 每天上午8点执行
        self.create_cron_schedule('generate_report', hour=8, minute=0)

        logger.info("生产环境定时任务设置完成")

    def disable_all_tasks(self):
        """禁用所有密钥轮换相关任务"""
        tasks = PeriodicTask.objects.filter(name__startswith='key_rotation_')
        for task in tasks:
            task.enabled = False
            task.save()
            logger.info(f"禁用任务: {task.name}")

        logger.info(f"已禁用 {tasks.count()} 个密钥轮换任务")

    def enable_all_tasks(self):
        """启用所有密钥轮换相关任务"""
        tasks = PeriodicTask.objects.filter(name__startswith='key_rotation_')
        for task in tasks:
            task.enabled = True
            task.save()
            logger.info(f"启用任务: {task.name}")

        logger.info(f"已启用 {tasks.count()} 个密钥轮换任务")

    def list_tasks(self):
        """列出所有密钥轮换相关任务"""
        tasks = PeriodicTask.objects.filter(name__startswith='key_rotation_')

        task_list = []
        for task in tasks:
            schedule_info = ""
            if task.interval:
                schedule_info = f"每{task.interval.every}{task.interval.period}"
            elif task.crontab:
                schedule_info = f"Cron: {task.crontab.minute} {task.crontab.hour} * * {task.crontab.day_of_week}"

            task_info = {
                'name': task.name,
                'task': task.task,
                'enabled': task.enabled,
                'schedule': schedule_info,
                'description': task.description or '',
                'last_run': task.last_run_at.isoformat() if task.last_run_at else None,
                'total_runs': task.total_run_count
            }
            task_list.append(task_info)

        return task_list

    def delete_task(self, task_name):
        """删除指定的定时任务"""
        try:
            task = PeriodicTask.objects.get(name=f"key_rotation_{task_name}")
            task.delete()
            logger.info(f"删除任务: key_rotation_{task_name}")
            return True
        except PeriodicTask.DoesNotExist:
            logger.warning(f"任务不存在: key_rotation_{task_name}")
            return False

    def update_task_args(self, task_name, **kwargs):
        """更新任务参数"""
        try:
            task = PeriodicTask.objects.get(name=f"key_rotation_{task_name}")
            if kwargs:
                task.kwargs = json.dumps(kwargs)
                task.save()
                logger.info(f"更新任务参数: {task.name} - {kwargs}")
            return True
        except PeriodicTask.DoesNotExist:
            logger.warning(f"任务不存在: key_rotation_{task_name}")
            return False


def main():
    """主函数 - 命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description='密钥轮换定时调度器')
    parser.add_argument('command', choices=[
        'setup-default', 'setup-production', 'list', 'enable-all',
        'disable-all', 'create', 'delete', 'update'
    ], help='执行的命令')

    # 创建任务的参数
    parser.add_argument('--task-name', help='任务名称')
    parser.add_argument('--interval', type=int, help='间隔值')
    parser.add_argument('--interval-type', choices=['minutes', 'hours', 'days'], help='间隔类型')
    parser.add_argument('--hour', type=int, help='Cron小时')
    parser.add_argument('--minute', type=int, help='Cron分钟')
    parser.add_argument('--day-of-week', help='Cron星期')
    parser.add_argument('--enabled', action='store_true', help='启用任务')
    parser.add_argument('--disabled', action='store_true', help='禁用任务')

    args = parser.parse_args()

    scheduler = KeyRotationScheduler()

    try:
        if args.command == 'setup-default':
            scheduler.setup_default_schedules()

        elif args.command == 'setup-production':
            scheduler.setup_production_schedules()

        elif args.command == 'list':
            tasks = scheduler.list_tasks()
            print("\n密钥轮换定时任务:")
            print("-" * 80)
            for task in tasks:
                status = "✓" if task['enabled'] else "✗"
                print(f"{status} {task['name']}")
                print(f"   任务: {task['task']}")
                print(f"   调度: {task['schedule']}")
                print(f"   描述: {task['description']}")
                print(f"   运行次数: {task['total_runs']}")
                if task['last_run']:
                    print(f"   上次运行: {task['last_run']}")
                print()

        elif args.command == 'enable-all':
            scheduler.enable_all_tasks()

        elif args.command == 'disable-all':
            scheduler.disable_all_tasks()

        elif args.command == 'create':
            if not args.task_name:
                print("错误: 必须指定 --task-name")
                return

            enabled = not args.disabled if args.enabled or args.disabled else True

            if args.hour is not None or args.minute is not None:
                # 创建Cron任务
                scheduler.create_cron_schedule(
                    args.task_name,
                    hour=args.hour or 0,
                    minute=args.minute or 0,
                    day_of_week=args.day_of_week or '*',
                    enabled=enabled
                )
            else:
                # 创建间隔任务
                scheduler.create_or_update_schedule(
                    args.task_name,
                    interval_value=args.interval,
                    interval_type=args.interval_type,
                    enabled=enabled
                )

        elif args.command == 'delete':
            if not args.task_name:
                print("错误: 必须指定 --task-name")
                return

            success = scheduler.delete_task(args.task_name)
            if not success:
                print(f"删除任务失败: {args.task_name}")

        elif args.command == 'update':
            if not args.task_name:
                print("错误: 必须指定 --task-name")
                return

            # TODO: 实现更新逻辑
            print("更新功能待实现")

    except Exception as e:
        logger.error(f"执行命令失败: {e}")
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
