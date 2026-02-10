import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, CheckCircle } from 'lucide-react';

const Dashboard = () => {
    const navigate = useNavigate();
    const { token, logout, loading, isAdmin } = useAuth();

    useEffect(() => {
        if (!loading && !token) {
            navigate('/login');
        }
    }, [token, loading, navigate]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    if (loading) return <div className="subtitle">Loading...</div>;
    if (!token) return null;

    return (
        <div className="glass-card" style={{ maxWidth: '500px' }}>
            <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                <CheckCircle size={64} color="#22c55e" style={{ margin: '0 auto' }} />
            </div>
            <h1>Success!</h1>
            <p className="subtitle">You have successfully logged into the system.</p>

            <div style={{ background: 'rgba(15, 23, 42, 0.4)', padding: '1.5rem', borderRadius: '1rem', marginTop: '1.5rem' }}>
                <h3 style={{ marginBottom: '0.75rem', fontSize: '1rem', color: '#94a3b8' }}>Token Information</h3>
                <p style={{ wordBreak: 'break-all', fontSize: '0.75rem', color: '#cbd5e1', fontFamily: 'monospace' }}>
                    {token}
                </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '2rem' }}>
                {isAdmin && (
                    <button
                        className="btn-primary"
                        onClick={() => navigate('/admin')}
                        style={{ background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)', boxShadow: '0 4px 15px rgba(99, 102, 241, 0.3)' }}
                    >
                        Admin Panel
                    </button>
                )}

                <button className="btn-primary" onClick={handleLogout} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
                    <LogOut size={18} />
                    Sign Out
                </button>
            </div>
        </div>
    );
};

export default Dashboard;
