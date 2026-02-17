import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'
});

api.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('access_token');
  const csrfToken = localStorage.getItem('csrf_token') ?? 'csrf-demo-token';
  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;
  config.headers['X-CSRF-Token'] = csrfToken;
  return config;
});
