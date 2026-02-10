import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { authService } from '../api/auth';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(authService.getToken());
    const [loading, setLoading] = useState(true);

    const fetchProfile = useCallback(async () => {
        try {
            const profile = await authService.getProfile();
            setUser(profile);
        } catch (error) {
            console.error('Failed to fetch profile:', error);
            logout();
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        const storedToken = authService.getToken();
        if (storedToken) {
            setToken(storedToken);
            fetchProfile();
        } else {
            setLoading(false);
        }
    }, [fetchProfile]);

    const login = async (username, password) => {
        const data = await authService.login(username, password);
        setToken(data.access_token);
        // Fetch full profile after login to get the role
        await fetchProfile();
        return data;
    };

    const googleLogin = async (googleToken) => {
        const data = await authService.googleLogin(googleToken);
        setToken(data.token.access_token);
        await fetchProfile();
        return data;
    };

    const signup = async (userData) => {
        const data = await authService.signup(userData);
        if (data.token?.access_token) {
            setToken(data.token.access_token);
            // Profile is already in the signup response, but we can fetch it to be sure
            // or just set it: setUser(data.user);
            setUser(data.user);
        }
        return data;
    };

    const logout = () => {
        authService.logout();
        setToken(null);
        setUser(null);
    };

    const isAdmin = user?.role === 'admin';

    return (
        <AuthContext.Provider value={{ user, token, loading, login, googleLogin, signup, logout, isAdmin }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
