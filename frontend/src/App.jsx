import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import VIPArea from './components/VIPArea';

export default function App() {
  const [user, setUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);

  const handleRegisterSuccess = () => {
    setShowRegister(false);
  };

  return (
    <div>
      {!user ? (
        <div>
          {showRegister ? (
            <div>
              <Register onRegisterSuccess={handleRegisterSuccess} />
              <p>
                Já tem conta? <button onClick={() => setShowRegister(false)}>Fazer Login</button>
              </p>
            </div>
          ) : (
            <div>
              <Login onLogin={setUser} />
              <p>
                Não tem conta? <button onClick={() => setShowRegister(true)}>Cadastrar</button>
              </p>
            </div>
          )}
        </div>
      ) : (
        <VIPArea user={user} onLogout={() => setUser(null)} />
      )}
    </div>
  );
}