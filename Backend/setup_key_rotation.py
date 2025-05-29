#!/usr/bin/env python3
"""
密钥轮换系统快速设置脚本
自动配置和启动密钥轮换系统
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class KeyRotationSetup:
    """密钥轮换系统设置器"""

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.env_file = self.base_dir / '.env'
        self.backup_dir = self.base_dir / 'key_backups'

    def check_dependencies(self):
        """检查系统依赖"""
        print("🔍 检查系统依赖...")

        dependencies = [
            ('django', 'Django'),
            ('celery', 'Celery'),
            ('redis', 'Redis'),
            ('django_celery_beat', 'Django-Celery-Beat'),
        ]

        missing_deps = []

        for module, name in dependencies:
            try:
                __import__(module)
                print(f"  ✓ {name}")
            except ImportError:
                print(f"  ✗ {name} - 未安装")
                missing_deps.append(name.lower())

        if missing_deps:
            print(f"\n❌ 缺少依赖: {', '.join(missing_deps)}")
            print("请运行以下命令安装:")
            print(f"pip install {' '.join(missing_deps)}")
            return False

        print("✅ 所有依赖已安装")
        return True

    def check_redis_connection(self):
        """检查Redis连接"""
        print("\n🔍 检查Redis连接...")

        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            print("  ✓ Redis连接正常")
            return True
        except Exception as e:
            print(f"  ✗ Redis连接失败: {e}")
            print("请确保Redis服务正在运行:")
            print("  sudo systemctl start redis")
            print("  或 brew services start redis (macOS)")
            return False

    def setup_directories(self):
        """创建必要的目录"""
        print("\n📁 创建目录结构...")

        directories = [
            self.backup_dir,
            self.base_dir / 'logs',
            self.base_dir / 'apps' / 'core' / 'management',
            self.base_dir / 'apps' / 'core' / 'management' / 'commands',
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {directory}")

        # 创建__init__.py文件
        init_files = [
            self.base_dir / 'apps' / 'core' / 'management' / '__init__.py',
            self.base_dir / 'apps' / 'core' / 'management' / 'commands' / '__init__.py',
        ]

        for init_file in init_files:
            if not init_file.exists():
                init_file.touch()
                print(f"  ✓ {init_file}")

    def check_env_file(self):
        """检查环境文件"""
        print("\n📋 检查环境文件...")

        if not self.env_file.exists():
            print("  ✗ .env文件不存在")

            # 询问是否要生成新的.env文件
            response = input("是否要生成新的.env文件? (y/n): ").lower().strip()
            if response == 'y':
                self.generate_env_file()
            else:
                print("请手动创建.env文件或运行 python generate_keys.py")
                return False
        else:
            print("  ✓ .env文件存在")

            # 检查关键配置
            with open(self.env_file, 'r') as f:
                content = f.read()

            if 'KEY_ROTATION_ENABLED' in content:
                print("  ✓ 包含密钥轮换配置")
            else:
                print("  ⚠ 缺少密钥轮换配置，请检查.env文件")

        return True

    def generate_env_file(self):
        """生成新的环境文件"""
        print("  📝 生成新的.env文件...")

        try:
            # 执行generate_keys.py脚本
            result = subprocess.run([
                sys.executable, 'generate_keys.py'
            ], cwd=self.base_dir, capture_output=True, text=True)

            if result.returncode == 0:
                # 将生成的文件重命名为.env
                generated_file = self.base_dir / '.env.generated'
                if generated_file.exists():
                    generated_file.rename(self.env_file)
                    print("  ✓ .env文件生成成功")
                else:
                    print("  ✗ 生成的文件不存在")
                    return False
            else:
                print(f"  ✗ 生成失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"  ✗ 生成异常: {e}")
            return False

        return True

    def setup_django_settings(self):
        """设置Django配置"""
        print("\n⚙️ 配置Django设置...")

        # 检查INSTALLED_APPS中是否包含必要的应用
        settings_file = self.base_dir / 'backend' / 'settings.py'

        if not settings_file.exists():
            print("  ⚠ 未找到Django settings.py文件")
            return True

        with open(settings_file, 'r') as f:
            content = f.read()

        required_apps = [
            'django_celery_beat',
            'apps.core',
        ]

        missing_apps = []
        for app in required_apps:
            if app not in content:
                missing_apps.append(app)

        if missing_apps:
            print(f"  ⚠ INSTALLED_APPS中缺少: {', '.join(missing_apps)}")
            print("  请手动添加到Django settings.py的INSTALLED_APPS中")
        else:
            print("  ✓ Django配置正确")

        return True

    def setup_celery_tasks(self):
        """设置Celery定时任务"""
        print("\n⏰ 设置Celery定时任务...")

        try:
            # 设置Django环境
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

            import django
            django.setup()

            # 运行数据库迁移
            print("  📊 执行数据库迁移...")
            result = subprocess.run([
                sys.executable, 'manage.py', 'migrate'
            ], cwd=self.base_dir, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"  ⚠ 数据库迁移警告: {result.stderr}")
            else:
                print("  ✓ 数据库迁移完成")

            # 设置默认定时任务
            print("  ⚙️ 设置默认定时任务...")
            result = subprocess.run([
                sys.executable, 'key_scheduler.py', 'setup-default'
            ], cwd=self.base_dir, capture_output=True, text=True)

            if result.returncode == 0:
                print("  ✓ 定时任务设置成功")
            else:
                print(f"  ⚠ 定时任务设置警告: {result.stderr}")

        except Exception as e:
            print(f"  ⚠ Celery设置异常: {e}")

        return True

    def test_key_rotation(self):
        """测试密钥轮换功能"""
        print("\n🧪 测试密钥轮换功能...")

        try:
            # 验证当前密钥
            print("  🔍 验证当前密钥...")
            result = subprocess.run([
                sys.executable, 'manage.py', 'rotate_keys', '--validate-only'
            ], cwd=self.base_dir, capture_output=True, text=True)

            if result.returncode == 0:
                print("  ✓ 密钥验证通过")
            else:
                print(f"  ⚠ 密钥验证警告: {result.stderr}")

            # 模拟轮换
            print("  🔄 执行模拟轮换...")
            result = subprocess.run([
                sys.executable, 'manage.py', 'rotate_keys', '--dry-run'
            ], cwd=self.base_dir, capture_output=True, text=True)

            if result.returncode == 0:
                print("  ✓ 模拟轮换成功")
            else:
                print(f"  ⚠ 模拟轮换警告: {result.stderr}")

        except Exception as e:
            print(f"  ⚠ 测试异常: {e}")

        return True

    def generate_start_scripts(self):
        """生成启动脚本"""
        print("\n📜 生成启动脚本...")

        # Celery Worker启动脚本
        worker_script = self.base_dir / 'start_celery_worker.sh'
        with open(worker_script, 'w') as f:
            f.write("""#!/bin/bash
# Celery Worker启动脚本

echo "启动Celery Worker..."
celery -A backend worker -l info --concurrency=4
""")
        worker_script.chmod(0o755)
        print("  ✓ start_celery_worker.sh")

        # Celery Beat启动脚本
        beat_script = self.base_dir / 'start_celery_beat.sh'
        with open(beat_script, 'w') as f:
            f.write("""#!/bin/bash
# Celery Beat启动脚本

echo "启动Celery Beat定时任务..."
celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
""")
        beat_script.chmod(0o755)
        print("  ✓ start_celery_beat.sh")

        # Windows批处理文件
        worker_bat = self.base_dir / 'start_celery_worker.bat'
        with open(worker_bat, 'w') as f:
            f.write("""@echo off
echo 启动Celery Worker...
celery -A backend worker -l info --concurrency=4
pause
""")
        print("  ✓ start_celery_worker.bat")

        beat_bat = self.base_dir / 'start_celery_beat.bat'
        with open(beat_bat, 'w') as f:
            f.write("""@echo off
echo 启动Celery Beat定时任务...
celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
pause
""")
        print("  ✓ start_celery_beat.bat")

    def show_usage_instructions(self):
        """显示使用说明"""
        print("\n" + "="*60)
        print("🎉 密钥轮换系统设置完成!")
        print("="*60)

        print("\n📋 使用说明:")
        print("\n1. 启动Celery服务:")
        if os.name == 'nt':  # Windows
            print("   worker:  start_celery_worker.bat")
            print("   beat:    start_celery_beat.bat")
        else:  # Unix/Linux/macOS
            print("   worker:  ./start_celery_worker.sh")
            print("   beat:    ./start_celery_beat.sh")

        print("\n2. 手动执行密钥轮换:")
        print("   验证密钥:  python manage.py rotate_keys --validate-only")
        print("   模拟轮换:  python manage.py rotate_keys --dry-run")
        print("   强制轮换:  python manage.py rotate_keys --force")

        print("\n3. 管理定时任务:")
        print("   查看任务:  python key_scheduler.py list")
        print("   启用任务:  python key_scheduler.py enable-all")
        print("   禁用任务:  python key_scheduler.py disable-all")

        print("\n4. 命令行工具:")
        print("   生成密钥:  python key_rotation_manager.py generate")
        print("   创建备份:  python key_rotation_manager.py backup")
        print("   查看备份:  python key_rotation_manager.py list-backups")

        print("\n📚 详细文档: docs/key_rotation_guide.md")

        print("\n⚠️ 重要提醒:")
        print("- 首次使用前请阅读安全注意事项")
        print("- 密钥轮换后需要重启Django应用")
        print("- 建议在测试环境充分验证后再用于生产")
        print("- 定期检查和清理备份文件")

    def run_setup(self):
        """运行完整设置流程"""
        print("🚀 密钥轮换系统设置向导")
        print("="*50)

        steps = [
            ("检查依赖", self.check_dependencies),
            ("检查Redis", self.check_redis_connection),
            ("创建目录", self.setup_directories),
            ("检查环境文件", self.check_env_file),
            ("配置Django", self.setup_django_settings),
            ("设置Celery", self.setup_celery_tasks),
            ("测试功能", self.test_key_rotation),
            ("生成脚本", self.generate_start_scripts),
        ]

        failed_steps = []

        for step_name, step_func in steps:
            try:
                if not step_func():
                    failed_steps.append(step_name)
            except Exception as e:
                print(f"❌ {step_name} 失败: {e}")
                failed_steps.append(step_name)

        if failed_steps:
            print(f"\n⚠️ 部分步骤失败: {', '.join(failed_steps)}")
            print("请检查错误信息并手动修复")

        self.show_usage_instructions()


def main():
    """主函数"""
    setup = KeyRotationSetup()

    try:
        setup.run_setup()
    except KeyboardInterrupt:
        print("\n\n❌ 设置被用户取消")
    except Exception as e:
        print(f"\n❌ 设置过程发生错误: {e}")
        print("请检查错误信息并重试")


if __name__ == "__main__":
    main()
