import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const login = async (username: string, password: string) => {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
};

export const register = async (username: string, email: string, password: string) => {
  const response = await api.post('/auth/register', { username, email, password });
  return response.data;
};

// Student endpoints
export const getStudents = async () => {
  const response = await api.get('/students');
  return response.data;
};

export const addStudent = async (username: string, email: string, imageHash: string) => {
  const response = await api.post('/students/enroll', { username, email, image_hash: imageHash });
  return response.data;
};

// Attendance endpoints
export const markAttendance = async (studentId: number, date: string, status: string, confidence?: number) => {
  const response = await api.post('/attendance/mark', { studentId, date, status, confidence });
  return response.data;
};

export default api;
