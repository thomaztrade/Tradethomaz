import React from 'react';
import SignalChart from './SignalChart';

export default function VIPArea({ user, onLogout }) {
  return (
    <div style={{ padding: 20 }}>
      <h2>Bem-vindo, {user.email}</h2>
      <p>Você está na área VIP. Aqui estão os sinais em tempo real:</p>
      <button onClick={onLogout}>Sair</button>

      <hr />
      <SignalChart />
    </div>
  );
}