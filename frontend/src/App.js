import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom'; // Agrega useNavigate

import Login from './components/login';
import Servidores from './components/servidores';
import Home from './pages/home';
import Register from './pages/register';
import Navbar from './components/navbar';
import ProtectedRoute from './components/ProtectedRoute';

import './css/global.css';
import './css/login.css';
import './css/home.css';
import './css/servidores.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const navigate = useNavigate(); // Para redirigir después del login

  // Función para manejar el inicio de sesión
  const handleLogin = (newToken) => {
    console.log("Login triggered with token:", newToken);
    localStorage.setItem('token', newToken);
    setToken(newToken);
    navigate('/home'); // Redirigir a /home después del login
  };

  // Función para manejar el cierre de sesión
  const handleLogout = () => {
    console.log("Logout triggered");
    localStorage.removeItem('token');
    setToken(null);
    navigate('/login'); // Redirigir al login después del logout
  };

  // Verificar el token al cargar la aplicación
  useEffect(() => {
    console.log("useEffect triggered");
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
      console.log("Token found in localStorage:", savedToken);
      setToken(savedToken);
    } else {
      navigate('/login'); // Si no hay token, redirige al login
    }
  }, [navigate]); // Asegúrate de agregar el navigate en el array de dependencias

  console.log("Rendering App with token:", token);

  return (
    <>
      <Navbar isLoggedIn={!!token} onLogout={handleLogout} /> {/* Pasa el estado isLoggedIn */}
      <Routes>
        <Route path="/" element={<Login onLogin={handleLogin} />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/home"
          element={
            <ProtectedRoute token={token}>
              <Home onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/servidores"
          element={
            <ProtectedRoute token={token}>
              <Servidores token={token} />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

export default App;
