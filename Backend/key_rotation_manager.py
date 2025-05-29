#!/usr/bin/env python3
"""
密钥轮换管理器
为元宇宙社交平台提供自动化密钥轮换功能
支持定时轮换、备份恢复、安全更新等功能
"""

import os
import shutil
import secrets
import string
import json
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from threading import Timer
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('key_rotation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class KeyConfig:
    """密钥配置类"""
    name: str
    length: int
    key_type: str  # 'random', 'hex', 'base64', 'alphanumeric'
    description: str
    critical: bool = False  # 是否为关键密钥

class KeyRotationManager:
    """密钥轮换管理器"""

    def __init__(self, env_file: str = ".env", backup_dir: str = "key_backups"):
        self.env_file = Path(env_file)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

        # 密钥配置定义
        self.key_configs = {
            'CRYPTO_KEY': KeyConfig('CRYPTO_KEY', 64, 'random', '应用层加密主密钥', True),
            'CRYPTO_IV': KeyConfig('CRYPTO_IV', 16, 'alphanumeric', '应用层加密初始向量', True),
            'TRANSPORT_KEY': KeyConfig('TRANSPORT_KEY', 64, 'random', '传输层加密主密钥', True),
            'SECRET_KEY': KeyConfig('SECRET_KEY', 50, 'random', 'Django SECRET_KEY', True),
            'JWT_SECRET': KeyConfig('JWT_SECRET', 32, 'base64', 'JWT密钥', True),
            'API_KEY': KeyConfig('API_KEY', 16, 'hex', 'API密钥', False),
            'WEBHOOK_SECRET': KeyConfig('WEBHOOK_SECRET', 32, 'random', 'Webhook签名密钥', False),
            'LEGACY_CRYPTO_KEY': KeyConfig('LEGACY_CRYPTO_KEY', 64, 'random', '旧版加密密钥', False),
            'ENCRYPTION_CACHE_PREFIX': KeyConfig('ENCRYPTION_CACHE_PREFIX', 4, 'hex_prefix', '缓存键前缀', False),
        }

        # 加载当前配置
        self.current_config = self._load_env_config()

    def _load_env_config(self) -> Dict[str, str]:
        """加载当前环境配置"""
        config = {}
        if self.env_file.exists():
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value
        return config

    def _generate_key(self, key_config: KeyConfig) -> str:
        """根据配置生成密钥"""
        if key_config.key_type == 'random':
            alphabet = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}|;:,.<>?'
            return ''.join(secrets.choice(alphabet) for _ in range(key_config.length))
        elif key_config.key_type == 'hex':
            return secrets.token_hex(key_config.length)
        elif key_config.key_type == 'base64':
            return secrets.token_urlsafe(key_config.length)
        elif key_config.key_type == 'alphanumeric':
            alphabet = string.ascii_letters + string.digits
            return ''.join(secrets.choice(alphabet) for _ in range(key_config.length))
        elif key_config.key_type == 'hex_prefix':
            return f"encrypt_{secrets.token_hex(key_config.length)}:"
        else:
            raise ValueError(f"未知的密钥类型: {key_config.key_type}")

    def generate_new_keys(self, key_names: Optional[List[str]] = None) -> Dict[str, str]:
        """生成新密钥"""
        new_keys = {}
        keys_to_generate = key_names or list(self.key_configs.keys())

        for key_name in keys_to_generate:
            if key_name in self.key_configs:
                config = self.key_configs[key_name]
                new_keys[key_name] = self._generate_key(config)
                logger.info(f"生成新密钥: {key_name}")
            else:
                logger.warning(f"未知的密钥名称: {key_name}")

        return new_keys

    def create_backup(self) -> str:
        """创建当前配置的备份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f"env_backup_{timestamp}.env"

        if self.env_file.exists():
            shutil.copy2(self.env_file, backup_file)
            logger.info(f"创建备份: {backup_file}")

            # 创建备份元数据
            metadata = {
                'timestamp': timestamp,
                'original_file': str(self.env_file),
                'backup_file': str(backup_file),
                'file_size': backup_file.stat().st_size,
                'keys_count': len([k for k in self.current_config.keys() if k in self.key_configs])
            }

            metadata_file = self.backup_dir / f"backup_metadata_{timestamp}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            return str(backup_file)
        else:
            logger.error(f"环境文件不存在: {self.env_file}")
            return ""

    def update_env_file(self, new_keys: Dict[str, str], create_backup: bool = True) -> bool:
        """更新环境文件"""
        try:
            # 创建备份
            if create_backup:
                backup_file = self.create_backup()
                if not backup_file:
                    logger.error("无法创建备份，取消更新操作")
                    return False

            # 读取当前文件内容
            if self.env_file.exists():
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            else:
                lines = []

            # 更新密钥值
            updated_lines = []
            updated_keys = set()

            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and '=' in stripped:
                    key, _ = stripped.split('=', 1)
                    if key in new_keys:
                        updated_lines.append(f"{key}={new_keys[key]}\n")
                        updated_keys.add(key)
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)

            # 添加新的密钥（如果不存在）
            for key, value in new_keys.items():
                if key not in updated_keys:
                    if self.key_configs.get(key):
                        comment = f"# {self.key_configs[key].description}\n"
                        updated_lines.append(comment)
                    updated_lines.append(f"{key}={value}\n")

            # 更新生成时间注释
            timestamp_comment = f"# 密钥更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            if updated_lines and updated_lines[1].startswith('# 生成时间:'):
                updated_lines[1] = timestamp_comment
            elif updated_lines:
                updated_lines.insert(1, timestamp_comment)

            # 写入文件
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)

            logger.info(f"成功更新环境文件: {self.env_file}")
            logger.info(f"更新的密钥: {', '.join(new_keys.keys())}")

            # 更新内存中的配置
            self.current_config.update(new_keys)

            # 记录更新日志
            self._log_key_update(new_keys, backup_file if create_backup else None)

            return True

        except Exception as e:
            logger.error(f"更新环境文件失败: {e}")
            return False

    def _log_key_update(self, updated_keys: Dict[str, str], backup_file: Optional[str]):
        """记录密钥更新日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'updated_keys': list(updated_keys.keys()),
            'backup_file': backup_file,
            'critical_keys_updated': [k for k in updated_keys.keys()
                                    if self.key_configs.get(k, KeyConfig('', 0, '', '', False)).critical]
        }

        log_file = Path('key_update_history.json')
        history = []

        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                logger.warning("密钥更新历史文件损坏，创建新文件")

        history.append(log_entry)

        # 保留最近100条记录
        if len(history) > 100:
            history = history[-100:]

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def rotate_keys(self, key_names: Optional[List[str]] = None, force: bool = False) -> bool:
        """执行密钥轮换"""
        logger.info("开始密钥轮换操作")

        # 检查轮换条件
        if not force and not self._should_rotate():
            logger.info("未到轮换时间，跳过轮换")
            return True

        # 生成新密钥
        new_keys = self.generate_new_keys(key_names)
        if not new_keys:
            logger.error("未生成任何新密钥")
            return False

        # 更新环境文件
        success = self.update_env_file(new_keys)

        if success:
            logger.info("密钥轮换完成")
            # 清理旧备份
            self._cleanup_old_backups()
        else:
            logger.error("密钥轮换失败")

        return success

    def _should_rotate(self) -> bool:
        """检查是否应该进行密钥轮换"""
        # 读取轮换配置
        rotation_enabled = self.current_config.get('KEY_ROTATION_ENABLED', 'False').lower() == 'true'
        if not rotation_enabled:
            return False

        rotation_interval = int(self.current_config.get('KEY_ROTATION_INTERVAL', '24'))

        # 检查上次轮换时间
        history_file = Path('key_update_history.json')
        if not history_file.exists():
            return True

        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)

            if not history:
                return True

            last_update = datetime.fromisoformat(history[-1]['timestamp'])
            time_since_last = datetime.now() - last_update

            return time_since_last >= timedelta(hours=rotation_interval)

        except (json.JSONDecodeError, KeyError, ValueError):
            logger.warning("无法读取更新历史，执行轮换")
            return True

    def _cleanup_old_backups(self, keep_count: Optional[int] = None):
        """清理旧备份文件"""
        if keep_count is None:
            keep_count = int(self.current_config.get('KEY_BACKUP_COUNT', '3'))

        backup_files = sorted(
            [f for f in self.backup_dir.glob('env_backup_*.env')],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        # 删除超出保留数量的备份
        for backup_file in backup_files[keep_count:]:
            try:
                backup_file.unlink()
                # 同时删除对应的元数据文件
                metadata_file = backup_file.with_name(
                    backup_file.name.replace('env_backup_', 'backup_metadata_').replace('.env', '.json')
                )
                if metadata_file.exists():
                    metadata_file.unlink()
                logger.info(f"删除旧备份: {backup_file}")
            except OSError as e:
                logger.warning(f"删除备份文件失败: {backup_file}, 错误: {e}")

    def restore_from_backup(self, backup_file: str) -> bool:
        """从备份恢复配置"""
        backup_path = Path(backup_file)

        if not backup_path.exists():
            logger.error(f"备份文件不存在: {backup_file}")
            return False

        try:
            # 创建当前配置的备份
            current_backup = self.create_backup()

            # 恢复备份
            shutil.copy2(backup_path, self.env_file)
            logger.info(f"成功从备份恢复: {backup_file}")

            # 重新加载配置
            self.current_config = self._load_env_config()

            return True

        except Exception as e:
            logger.error(f"恢复备份失败: {e}")
            return False

    def list_backups(self) -> List[Dict[str, str]]:
        """列出所有备份"""
        backups = []

        for backup_file in sorted(self.backup_dir.glob('env_backup_*.env'), reverse=True):
            metadata_file = backup_file.with_name(
                backup_file.name.replace('env_backup_', 'backup_metadata_').replace('.env', '.json')
            )

            backup_info = {
                'file': str(backup_file),
                'timestamp': backup_file.stem.split('_', 2)[2],
                'size': backup_file.stat().st_size,
                'created': datetime.fromtimestamp(backup_file.stat().st_ctime).isoformat()
            }

            # 读取元数据
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        backup_info.update(metadata)
                except json.JSONDecodeError:
                    pass

            backups.append(backup_info)

        return backups

    def validate_keys(self) -> Dict[str, bool]:
        """验证当前密钥的有效性"""
        validation_results = {}

        for key_name, config in self.key_configs.items():
            current_value = self.current_config.get(key_name)

            if not current_value:
                validation_results[key_name] = False
                logger.warning(f"密钥缺失: {key_name}")
                continue

            # 验证长度和格式
            is_valid = True

            if config.key_type == 'hex' and len(current_value) != config.length * 2:
                is_valid = False
            elif config.key_type in ['random', 'alphanumeric'] and len(current_value) != config.length:
                is_valid = False
            elif config.key_type == 'hex_prefix' and not current_value.startswith('encrypt_'):
                is_valid = False

            validation_results[key_name] = is_valid

            if not is_valid:
                logger.warning(f"密钥格式无效: {key_name}")

        return validation_results

    def start_scheduled_rotation(self, interval_hours: Optional[int] = None):
        """启动定时密钥轮换"""
        if interval_hours is None:
            interval_hours = int(self.current_config.get('KEY_ROTATION_INTERVAL', '24'))

        def rotation_job():
            logger.info("执行定时密钥轮换")
            success = self.rotate_keys()
            if success:
                logger.info("定时密钥轮换成功")
            else:
                logger.error("定时密钥轮换失败")

            # 安排下次轮换
            timer = Timer(interval_hours * 3600, rotation_job)
            timer.daemon = True
            timer.start()

        # 启动首次轮换检查
        logger.info(f"启动定时密钥轮换，间隔: {interval_hours} 小时")
        timer = Timer(60, rotation_job)  # 1分钟后开始检查
        timer.daemon = True
        timer.start()

        return timer


def main():
    """主函数 - 命令行接口"""
    parser = argparse.ArgumentParser(description='密钥轮换管理器')
    parser.add_argument('--env-file', default='.env', help='环境文件路径')
    parser.add_argument('--backup-dir', default='key_backups', help='备份目录')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 生成密钥命令
    gen_parser = subparsers.add_parser('generate', help='生成新密钥')
    gen_parser.add_argument('--keys', nargs='*', help='指定要生成的密钥名称')
    gen_parser.add_argument('--output', help='输出文件路径')

    # 轮换密钥命令
    rotate_parser = subparsers.add_parser('rotate', help='执行密钥轮换')
    rotate_parser.add_argument('--keys', nargs='*', help='指定要轮换的密钥名称')
    rotate_parser.add_argument('--force', action='store_true', help='强制轮换')

    # 备份命令
    subparsers.add_parser('backup', help='创建配置备份')

    # 恢复命令
    restore_parser = subparsers.add_parser('restore', help='从备份恢复')
    restore_parser.add_argument('backup_file', help='备份文件路径')

    # 列出备份命令
    subparsers.add_parser('list-backups', help='列出所有备份')

    # 验证命令
    subparsers.add_parser('validate', help='验证密钥有效性')

    # 定时轮换命令
    schedule_parser = subparsers.add_parser('schedule', help='启动定时轮换')
    schedule_parser.add_argument('--interval', type=int, help='轮换间隔（小时）')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 创建管理器实例
    manager = KeyRotationManager(args.env_file, args.backup_dir)

    try:
        if args.command == 'generate':
            new_keys = manager.generate_new_keys(args.keys)

            if args.output:
                # 输出到指定文件
                with open(args.output, 'w', encoding='utf-8') as f:
                    for key, value in new_keys.items():
                        f.write(f"{key}={value}\n")
                print(f"新密钥已保存到: {args.output}")
            else:
                # 输出到控制台
                print("生成的新密钥:")
                for key, value in new_keys.items():
                    print(f"{key}={value}")

        elif args.command == 'rotate':
            success = manager.rotate_keys(args.keys, args.force)
            if success:
                print("密钥轮换成功")
            else:
                print("密钥轮换失败")
                exit(1)

        elif args.command == 'backup':
            backup_file = manager.create_backup()
            if backup_file:
                print(f"备份创建成功: {backup_file}")
            else:
                print("备份创建失败")
                exit(1)

        elif args.command == 'restore':
            success = manager.restore_from_backup(args.backup_file)
            if success:
                print(f"成功从备份恢复: {args.backup_file}")
            else:
                print("恢复失败")
                exit(1)

        elif args.command == 'list-backups':
            backups = manager.list_backups()
            if backups:
                print("可用备份:")
                for backup in backups:
                    print(f"  {backup['file']} - {backup['created']} ({backup['size']} bytes)")
            else:
                print("没有找到备份文件")

        elif args.command == 'validate':
            results = manager.validate_keys()
            all_valid = all(results.values())

            print("密钥验证结果:")
            for key, is_valid in results.items():
                status = "✓" if is_valid else "✗"
                print(f"  {status} {key}")

            if all_valid:
                print("所有密钥验证通过")
            else:
                print("存在无效密钥")
                exit(1)

        elif args.command == 'schedule':
            print("启动定时密钥轮换...")
            timer = manager.start_scheduled_rotation(args.interval)

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n停止定时轮换")
                timer.cancel()

    except Exception as e:
        logger.error(f"执行命令失败: {e}")
        exit(1)


if __name__ == "__main__":
    main()
