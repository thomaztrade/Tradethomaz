import React from 'react';
import SignalChart from './SignalChart';

export default function VIPArea({ user, onLogout }) {
  return (
    <div>
      <h2>Bem-vindo, {user.email}!</h2>
      <p>Esta é a área VIP do ThomazTrade.</p>
      <button onClick={onLogout}>Sair</button>
      <SignalChart />
    </div>
  );
}