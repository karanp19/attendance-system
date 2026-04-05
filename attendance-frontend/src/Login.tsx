import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface User {
  username: string;
  email: string;
}

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        username,
        password,
      });
      
      const { access_token, username: u, email } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify({ username: u, email }));
      
      setUser({ username: u, email });
      
      // Navigate to dashboard
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    window.location.href = '/';
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    }}>
      <div style={{
        width: '100%',
        maxWidth: '400px',
        padding: '20px',
      }}>
        <div className="card">
          <h1 style={{ textAlign: 'center', color: '#667eea', marginBottom: '24px' }}>
            Attendance System
          </h1>
          
          {user ? (
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>👤</div>
              <h2 style={{ color: '#333' }}>{user.username}</h2>
              <p style={{ color: '#666' }}>{user.email}</p>
              <button 
                className="btn btn-secondary"
                onClick={handleLogout}
                style={{ marginTop: '24px' }}
              >
                Logout
              </button>
            </div>
          ) : (
            <form onSubmit={handleLogin}>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', marginBottom: '8px', color: '#333' }}>
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="input"
                  placeholder="Enter username"
                  disabled={loading}
                />
              </div>
              
              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', marginBottom: '8px', color: '#333' }}>
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input"
                  placeholder="Enter password"
                  disabled={loading}
                />
              </div>
              
              {error && (
                <div className="error">
                  ⚠️ {error}
                </div>
              )}
              
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={loading}
                style={{ width: '100%', marginTop: '16px' }}
              >
                {loading ? 'Signing in...' : 'Login'}
              </button>
            </form>
          )}
        </div>
        
        <p style={{ 
          textAlign: 'center', 
          color: '#666', 
          marginTop: '16px',
          fontSize: '14px'
        }}>
          Default: admin / admin123
        </p>
      </div>
    </div>
  );
};

export default Login;
