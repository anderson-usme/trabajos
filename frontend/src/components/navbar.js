import React from 'react';
import { Link } from 'react-router-dom';

function Navbar({ isLoggedIn, onLogout }) {
  return (
    <nav className="navbar">
      <div className="navbar-links">
        {/* Mostrar "Registrar" siempre */}
        <Link to="/register" className="navbar-btn">Registrar</Link>

        {isLoggedIn && (
          <button onClick={onLogout} className="navbar-btn">Cerrar sesión</button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;



