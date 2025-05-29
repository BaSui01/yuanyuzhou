"""
Django管理命令：密钥轮换
使用方法：python manage.py rotate_keys [选项]
"""

import os
import sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path

# 添加项目根目录到Python路径，以便导入密钥管理器
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from key_rotation_manager import KeyRotationManager


class Command(BaseCommand):
    help = '执行密钥轮换操作'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keys',
            nargs='*',
            help='指定要轮换的密钥名称（空格分隔）'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制执行轮换，忽略时间间隔检查'
        )
        parser.add_argument(
            '--env-file',
            default='.env',
            help='环境文件路径（默认：.env）'
        )
        parser.add_argument(
            '--backup-dir',
            default='key_backups',
            help='备份目录（默认：key_backups）'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='模拟运行，不实际更新密钥'
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='仅验证当前密钥，不执行轮换'
        )

    def handle(self, *args, **options):
        """处理命令执行"""
        try:
            # 获取项目根目录
            base_dir = Path(settings.BASE_DIR)
            env_file = base_dir / options['env_file']
            backup_dir = base_dir / options['backup_dir']

            # 创建密钥管理器实例
            manager = KeyRotationManager(
                env_file=str(env_file),
                backup_dir=str(backup_dir)
            )

            # 验证密钥
            if options['validate_only']:
                self._validate_keys(manager)
                return

            # 模拟运行
            if options['dry_run']:
                self._dry_run(manager, options)
                return

            # 执行密钥轮换
            self._execute_rotation(manager, options)

        except Exception as e:
            raise CommandError(f'密钥轮换失败: {e}')

    def _validate_keys(self, manager):
        """验证密钥有效性"""
        self.stdout.write(self.style.HTTP_INFO('验证密钥有效性...'))

        validation_results = manager.validate_keys()
        all_valid = all(validation_results.values())

        self.stdout.write('\n密钥验证结果:')
        for key_name, is_valid in validation_results.items():
            if is_valid:
                self.stdout.write(f'  ✓ {key_name}', self.style.SUCCESS)
            else:
                self.stdout.write(f'  ✗ {key_name}', self.style.ERROR)

        if all_valid:
            self.stdout.write(
                self.style.SUCCESS('\n所有密钥验证通过')
            )
        else:
            self.stdout.write(
                self.style.WARNING('\n存在无效密钥，建议执行轮换')
            )

    def _dry_run(self, manager, options):
        """模拟运行"""
        self.stdout.write(self.style.HTTP_INFO('模拟密钥轮换...'))

        # 生成新密钥（但不保存）
        new_keys = manager.generate_new_keys(options['keys'])

        self.stdout.write('\n将要生成的新密钥:')
        for key_name in new_keys.keys():
            config = manager.key_configs.get(key_name)
            if config:
                status = "🔒 关键" if config.critical else "📝 普通"
                self.stdout.write(f'  {status} {key_name} - {config.description}')

        # 检查轮换条件
        should_rotate = manager._should_rotate()
        if should_rotate or options['force']:
            self.stdout.write(
                self.style.SUCCESS('\n✓ 满足轮换条件，可以执行轮换')
            )
        else:
            self.stdout.write(
                self.style.WARNING('\n⚠ 未到轮换时间，使用 --force 可强制轮换')
            )

        self.stdout.write(
            self.style.HTTP_INFO('\n模拟完成，未执行实际轮换')
        )

    def _execute_rotation(self, manager, options):
        """执行密钥轮换"""
        self.stdout.write(self.style.HTTP_INFO('开始密钥轮换...'))

        # 显示轮换信息
        if options['keys']:
            self.stdout.write(f"指定轮换密钥: {', '.join(options['keys'])}")
        else:
            self.stdout.write("轮换所有配置的密钥")

        # 执行轮换
        success = manager.rotate_keys(
            key_names=options['keys'],
            force=options['force']
        )

        if success:
            self.stdout.write(
                self.style.SUCCESS('✓ 密钥轮换成功完成')
            )

            # 显示备份信息
            backups = manager.list_backups()
            if backups:
                latest_backup = backups[0]
                self.stdout.write(
                    f"备份文件: {latest_backup['file']}"
                )

            # 提醒重启服务
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠ 重要提醒: 密钥已更新，请重启Django应用以加载新密钥'
                )
            )

        else:
            self.stdout.write(
                self.style.ERROR('✗ 密钥轮换失败')
            )
            sys.exit(1)

    def _show_backups(self, manager):
        """显示备份列表"""
        backups = manager.list_backups()

        if not backups:
            self.stdout.write('没有找到备份文件')
            return

        self.stdout.write('\n可用备份:')
        for backup in backups[:5]:  # 显示最近5个备份
            created_time = backup.get('created', '未知')
            file_size = backup.get('size', 0)
            self.stdout.write(
                f"  📁 {backup['file']} ({file_size} bytes) - {created_time}"
            )

        if len(backups) > 5:
            self.stdout.write(f"  ... 还有 {len(backups) - 5} 个备份文件")
