import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8005';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  signup: (email: string, password: string, full_name?: string) =>
    api.post('/api/auth/signup', { email, password, full_name }),
  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),
  getMe: () => api.get('/api/auth/me'),
};

export const messagesAPI = {
  create: (data: any) => api.post('/api/messages/', data),
  getAll: () => api.get('/api/messages/'),
  getOne: (id: number) => api.get(`/api/messages/${id}`),
  delete: (id: number) => api.delete(`/api/messages/${id}`),
};

export const companionAPI = {
  chat: (message: string) => api.post('/api/companion/chat', { message }),
  updatePersonality: (personality: string, custom_instructions?: string) =>
    api.put('/api/companion/personality', { personality, custom_instructions }),
  getDailyCheckin: () => api.get('/api/companion/daily-checkin'),
  helpCraftMessage: (intent: string) =>
    api.post('/api/companion/help-craft-message', { intent }),
};

export default api;
