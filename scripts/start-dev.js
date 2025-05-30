#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('🚀 启动完整开发环境...\n');

// 项目根目录
const projectRoot = path.join(__dirname, '..');
const backendDir = path.join(projectRoot, 'Backend');
const frontendDir = path.join(projectRoot, 'frontend');

// 检查目录是否存在
if (!fs.existsSync(backendDir)) {
    console.error('❌ 后端目录不存在:', backendDir);
    process.exit(1);
}

if (!fs.existsSync(frontendDir)) {
    console.error('❌ 前端目录不存在:', frontendDir);
    process.exit(1);
}

const processes = [];

// 启动后端 Django 服务器
console.log('🔧 启动后端 Django 服务器...');
const djangoProcess = spawn('python', ['manage.py', 'runserver', '127.0.0.1:8000'], {
    cwd: backendDir,
    stdio: 'pipe',
    shell: true,
    env: {
        ...process.env,
        PYTHONPATH: backendDir,
        DJANGO_SETTINGS_MODULE: 'backend.settings',
        DEBUG: 'True'
    }
});

djangoProcess.stdout.on('data', (data) => {
    console.log(`[Django] ${data.toString().trim()}`);
});

djangoProcess.stderr.on('data', (data) => {
    console.error(`[Django Error] ${data.toString().trim()}`);
});

processes.push(djangoProcess);

// 启动前端 Vite 开发服务器
console.log('🌐 启动前端 Vite 开发服务器...');
const viteProcess = spawn('npm', ['run', 'dev'], {
    cwd: frontendDir,
    stdio: 'pipe',
    shell: true,
    env: {
        ...process.env,
        NODE_ENV: 'development'
    }
});

viteProcess.stdout.on('data', (data) => {
    console.log(`[Vite] ${data.toString().trim()}`);
});

viteProcess.stderr.on('data', (data) => {
    console.error(`[Vite Error] ${data.toString().trim()}`);
});

processes.push(viteProcess);

// 可选：启动 Celery Worker
const startCelery = process.argv.includes('--celery') || process.argv.includes('-c');
if (startCelery) {
    console.log('🔄 启动 Celery Worker...');
    const celeryProcess = spawn('python', ['manage.py', 'celery', 'worker', '--loglevel=info'], {
        cwd: backendDir,
        stdio: 'pipe',
        shell: true,
        env: {
            ...process.env,
            PYTHONPATH: backendDir,
            DJANGO_SETTINGS_MODULE: 'backend.settings'
        }
    });

    celeryProcess.stdout.on('data', (data) => {
        console.log(`[Celery] ${data.toString().trim()}`);
    });

    celeryProcess.stderr.on('data', (data) => {
        console.error(`[Celery Error] ${data.toString().trim()}`);
    });

    processes.push(celeryProcess);
}

// 优雅退出处理
const cleanup = () => {
    console.log('\n🛑 正在关闭所有服务...');

    processes.forEach((proc, index) => {
        if (proc && !proc.killed) {
            const serviceName = index === 0 ? 'Django' : index === 1 ? 'Vite' : 'Celery';
            console.log(`🔴 关闭 ${serviceName} 服务...`);

            // 尝试优雅关闭
            proc.kill('SIGTERM');

            // 如果5秒后还没关闭，强制关闭
            setTimeout(() => {
                if (!proc.killed) {
                    console.log(`⚡ 强制关闭 ${serviceName} 服务...`);
                    proc.kill('SIGKILL');
                }
            }, 5000);
        }
    });

    setTimeout(() => {
        console.log('✅ 所有服务已关闭');
        process.exit(0);
    }, 6000);
};

// 监听退出信号
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('exit', cleanup);

// 监听进程退出
processes.forEach((proc, index) => {
    proc.on('exit', (code, signal) => {
        const serviceName = index === 0 ? 'Django' : index === 1 ? 'Vite' : 'Celery';
        if (code === 0) {
            console.log(`✅ ${serviceName} 服务正常退出`);
        } else {
            console.error(`❌ ${serviceName} 服务异常退出，代码: ${code}, 信号: ${signal}`);
        }
    });
});

console.log(`
📋 开发环境信息:
   - Django 后端: http://127.0.0.1:8000
   - Vite 前端: http://localhost:5173 (通常)
   - Django Admin: http://127.0.0.1:8000/admin
   - API 文档: http://127.0.0.1:8000/api/docs/
   ${startCelery ? '- Celery Worker: 已启动' : '- Celery Worker: 未启动 (使用 --celery 参数启动)'}

💡 使用提示:
   - 按 Ctrl+C 退出所有服务
   - 使用 --celery 或 -c 参数同时启动 Celery Worker
   - 日志会显示服务前缀: [Django], [Vite], [Celery]

🔧 开发工具:
   - Django Shell: python manage.py shell
   - 数据库迁移: python manage.py migrate
   - 创建超级用户: python manage.py createsuperuser
   - 前端代码检查: npm run lint
   - 前端代码格式化: npm run format
`);
