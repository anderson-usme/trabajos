import React, { useState } from 'react';
import axios from 'axios';
import '../css/login.css';  

function Login({ onLogin }) {
  const [username, setUsername] = useState('');  
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      // Realizar la solicitud POST al backend Django para obtener el token
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username,  
        password, 
      });

      // Si la respuesta es exitosa, pasa el token de acceso a la función onLogin
      onLogin(response.data.access);  // Cambiado a response.data.access
      setError('');  
    } catch (err) {
      
      setError('Credenciales incorrectas. Intenta nuevamente.');
    }
  };

  return (
    <div className="login">
      <h2>Iniciar sesión</h2>
      <input
        type="text"  
        placeholder="Nombre de usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Contraseña"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Iniciar sesión</button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Login;




