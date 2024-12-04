import React from 'react';
import '../css/home.css';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home-container">
      <h1>Bienvenido a la Administración de Servidores</h1>
      <nav>
        <Link to="/register">Registrar Usuario</Link>
        <Link to="/servidores">Gestionar Servidores</Link>
      </nav>
    </div>
  );
}

export default Home;

