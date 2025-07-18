import React, { useState } from 'react';
import Login from './components/Login';
import VIPArea from './components/VIPArea';

export default function App() {
  const [user, setUser] = useState(null);

  return (
    <div>
      {!user ? (
        <Login onLogin={setUser} />
      ) : (
        <VIPArea user={user} onLogout={() => setUser(null)} />
      )}
    </div>
  );
}