import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Users, Database, AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Admin = () => {
    const { user, token } = useAuth();
    const [stats, setStats] = useState({ users: 0, status: 'Active' });
    const navigate = useNavigate();

    return (
        <div className="glass-card" style={{ maxWidth: '800px', width: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <Shield size={40} color="#6366f1" />
                <div>
                    <h1 style={{ margin: 0 }}>Admin Panel</h1>
                    <p className="subtitle" style={{ margin: 0 }}>System Management & Monitoring</p>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1.5rem', borderRadius: '1rem', textAlign: 'center' }}>
                    <Users size={24} color="#a5b4fc" style={{ marginBottom: '0.5rem' }} />
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{user?.username}</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Current Session</div>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1.5rem', borderRadius: '1rem', textAlign: 'center' }}>
                    <Shield size={24} color="#fcd34d" style={{ marginBottom: '0.5rem' }} />
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#fcd34d' }}>{user?.role.toUpperCase()}</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Access Level</div>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1.5rem', borderRadius: '1rem', textAlign: 'center' }}>
                    <Database size={24} color="#34d399" style={{ marginBottom: '0.5rem' }} />
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#34d399' }}>Online</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Database Status</div>
                </div>
            </div>

            <div style={{ background: 'rgba(15, 23, 42, 0.4)', padding: '1.5rem', borderRadius: '1rem', marginBottom: '2.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                    <AlertTriangle size={20} color="#f87171" />
                    <h3 style={{ margin: 0, color: '#f87171' }}>System Logs Observation</h3>
                </div>
                <p style={{ color: '#cbd5e1', fontSize: '0.9rem', lineHeight: '1.6' }}>
                    To directly observe the full database records as requested, you can access the backend's generated view:
                </p>
                <div style={{ marginTop: '1rem' }}>
                    <a
                        href="http://localhost:8000/admin/users"
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                            display: 'inline-block',
                            background: '#6366f1',
                            color: 'white',
                            padding: '0.75rem 1.25rem',
                            borderRadius: '0.5rem',
                            textDecoration: 'none',
                            fontWeight: '600'
                        }}
                    >
                        Open Database View &rarr;
                    </a>
                </div>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
                <button className="btn-primary" onClick={() => navigate('/dashboard')}>
                    Back to Dashboard
                </button>
            </div>
        </div>
    );
};

export default Admin;
