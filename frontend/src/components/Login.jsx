import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogIn, User, Lock } from 'lucide-react';
import { GoogleLogin } from '@react-oauth/google';

const Login = () => {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const { login, googleLogin } = useAuth();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await login(formData.username, formData.password);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Invalid username or password');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card">
            <h1>Welcome Back</h1>
            <p className="subtitle">Please enter your details</p>

            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label htmlFor="username">Username</label>
                    <div style={{ position: 'relative' }}>
                        <span style={{ position: 'absolute', left: '12px', top: '10px', color: '#94a3b8' }}>
                            <User size={18} />
                        </span>
                        <input
                            className="input-field"
                            style={{ paddingLeft: '40px' }}
                            type="text"
                            id="username"
                            name="username"
                            placeholder="Enter your username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                        />
                    </div>
                </div>

                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <div style={{ position: 'relative' }}>
                        <span style={{ position: 'absolute', left: '12px', top: '10px', color: '#94a3b8' }}>
                            <Lock size={18} />
                        </span>
                        <input
                            className="input-field"
                            style={{ paddingLeft: '40px' }}
                            type="password"
                            id="password"
                            name="password"
                            placeholder="••••••••"
                            value={formData.password}
                            onChange={handleChange}
                            required
                        />
                    </div>
                </div>

                {error && <p className="error-msg">{error}</p>}

                <button className="btn-primary" type="submit" disabled={loading}>
                    {loading ? 'Signing in...' : 'Sign in'}
                </button>
            </form>

            <div style={{ margin: '20px 0', textAlign: 'center', color: '#94a3b8', fontSize: '0.9rem', position: 'relative' }}>
                <div style={{ position: 'absolute', top: '50%', left: 0, right: 0, height: '1px', background: 'rgba(148, 163, 184, 0.2)', zIndex: 0 }}></div>
                <span style={{ position: 'relative', background: 'rgba(255, 255, 255, 0.05)', padding: '0 10px', backdropFilter: 'blur(10px)', zIndex: 1 }}>or</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <GoogleLogin
                    onSuccess={async (credentialResponse) => {
                        setLoading(true);
                        setError('');
                        try {
                            await googleLogin(credentialResponse.credential);
                            navigate('/dashboard');
                        } catch (err) {
                            setError(err.response?.data?.detail || 'Google Login failed');
                        } finally {
                            setLoading(false);
                        }
                    }}
                    onError={() => {
                        setError('Google Login failed');
                    }}
                    useOneTap
                    theme="filled_blue"
                    shape="pill"
                />
            </div>

            <div className="auth-footer">
                Don't have an account?{' '}
                <Link to="/signup" className="auth-link">Sign up</Link>
            </div>
        </div>
    );
};

export default Login;
