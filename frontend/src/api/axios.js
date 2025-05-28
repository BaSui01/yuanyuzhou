import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// 创建axios实例
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 请求拦截器
axiosInstance.interceptors.request.use(
  config => {
    // 从store获取token（如果存在）
    const authStore = useAuthStore();
    const token = authStore.token;

    // 如果token存在，添加到请求头
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
axiosInstance.interceptors.response.use(
  response => {
    // 直接返回响应数据
    return response.data;
  },
  error => {
    const authStore = useAuthStore();

    // 处理错误响应
    if (error.response) {
      const { status, data } = error.response;

      // 处理401未授权错误（token过期或无效）
      if (status === 401) {
        console.warn('认证失败，请重新登录');
        // 清除token并重定向到登录页
        authStore.logout();
      }

      // 处理403权限不足错误
      if (status === 403) {
        console.warn('权限不足，无法访问该资源');
      }

      // 处理500服务器错误
      if (status >= 500) {
        console.error('服务器错误，请稍后再试');
      }

      // 返回错误信息
      return Promise.reject({
        status,
        message: data.message || '请求失败',
        data: data
      });
    }

    // 处理请求超时
    if (error.code === 'ECONNABORTED' && error.message.includes('timeout')) {
      console.error('请求超时，请检查网络连接');
      return Promise.reject({
        status: 408,
        message: '请求超时，请检查网络连接'
      });
    }

    // 处理网络错误
    if (!window.navigator.onLine) {
      console.error('网络连接已断开，请检查网络设置');
      return Promise.reject({
        status: -1,
        message: '网络连接已断开，请检查网络设置'
      });
    }

    // 其他错误
    console.error('请求错误:', error);
    return Promise.reject({
      status: -1,
      message: error.message || '未知错误'
    });
  }
);

export default axiosInstance;
