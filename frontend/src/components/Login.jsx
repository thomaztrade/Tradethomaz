import React, { useState } from 'react';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();

    // Login fixo: você pode mudar depois
    if (email === 'vip@exemplo.com' && senha === '123456') {
      onLogin({ email });
    } else {
      alert('Email ou senha incorretos.');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Área de Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Digite seu e-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br /><br />
        <input
          type="password"
          placeholder="Digite sua senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          required
        /><br /><br />
        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}