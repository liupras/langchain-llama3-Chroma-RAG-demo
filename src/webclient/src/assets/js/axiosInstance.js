import axios from 'axios';
import {getToken,logout} from '@/assets/js/auth';

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 90000,
});

// 请求拦截器：添加 Authorization 头
instance.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：处理 401 错误
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      logout();
    }
    return Promise.reject(error);
  }
);

export default instance;
