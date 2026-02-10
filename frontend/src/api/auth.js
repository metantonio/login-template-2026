import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const authService = {
    login: async (username, password) => {
        const response = await api.post('/login', { username, password });
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
        }
        return response.data;
    },

    signup: async (userData) => {
        const response = await api.post('/signup', userData);
        if (response.data.token?.access_token) {
            localStorage.setItem('token', response.data.token.access_token);
        }
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
    },

    getToken: () => {
        return localStorage.getItem('token');
    },

    getProfile: async () => {
        const token = localStorage.getItem('token');
        if (!token) throw new Error('No token found');

        const response = await api.get('/me', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    }
};
