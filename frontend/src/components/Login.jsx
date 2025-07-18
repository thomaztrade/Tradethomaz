import React, { useState } from 'react';
import axios from 'axios';

function Login({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const endpoint = isLogin ? '/api/login' : '/api/register';
      const response = await axios.post(endpoint, {
        email,
        password
      });

      if (isLogin) {
        onLogin({
          email,
          is_vip: response.data.is_vip,
          ...response.data.user
        });
        setMessage('Login realizado com sucesso!');
      } else {
        setMessage('Usuário registrado com sucesso! Faça login agora.');
        setIsLogin(true);
        setPassword('');
      }
    } catch (error) {
      if (error.response?.data?.message) {
        setMessage(error.response.data.message);
      } else {
        setMessage('Erro de conexão. Tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '400px', margin: '0 auto' }}>
      <h2>{isLogin ? 'Login' : 'Registro'}</h2>
      
      {message && (
        <div className={message.includes('sucesso') ? 'success' : 'error'}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Senha:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
            minLength={6}
          />
        </div>

        <button 
          type="submit" 
          className="btn"
          disabled={loading}
          style={{ width: '100%', marginBottom: '1rem' }}
        >
          {loading ? 'Processando...' : (isLogin ? 'Entrar' : 'Registrar')}
        </button>
      </form>

      <div style={{ textAlign: 'center' }}>
        <button
          type="button"
          onClick={() => {
            setIsLogin(!isLogin);
            setMessage('');
            setPassword('');
          }}
          className="btn btn-secondary"
          disabled={loading}
        >
          {isLogin ? 'Criar conta' : 'Já tenho conta'}
        </button>
      </div>

      <div style={{ marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '6px' }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>Sobre o ThomazTrade</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ marginBottom: '0.5rem' }}>📈 Sinais automatizados de trading</li>
          <li style={{ marginBottom: '0.5rem' }}>🔔 Notificações via Telegram</li>
          <li style={{ marginBottom: '0.5rem' }}>📊 Análise técnica avançada</li>
          <li style={{ marginBottom: '0.5rem' }}>📱 Interface web responsiva</li>
          <li style={{ marginBottom: '0.5rem' }}>⭐ Área VIP com recursos exclusivos</li>
        </ul>
      </div>
    </div>
  );
}

export default Login;