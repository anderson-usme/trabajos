import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import '../css/servidores.css'; 

function Servidores({ token }) {
  const [servidores, setServidores] = useState([]);
  const [nuevoServidor, setNuevoServidor] = useState({
    name: '',
    location: '',
    backendUrl: '',
    frontendUrl: '',
  });
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [statusGeneral, setStatusGeneral] = useState('');  // Estado para el status general

  const fetchServidores = useCallback(async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/check_url/', {  // Asegúrate que esté en el puerto correcto
        headers: { Authorization: `Bearer ${token}` },
      });
      setServidores(response.data.data);
      setStatusGeneral(response.data.status_general);  // Obtener y actualizar el estado general
      setMensaje('');
    } catch (err) {
      setError('Error al cargar los servidores.');
    }
  }, [token]);  // Dependencia de token

  const agregarServidor = async () => {
    if (!nuevoServidor.name || !nuevoServidor.location || !nuevoServidor.backendUrl || !nuevoServidor.frontendUrl) {
      setError('Todos los campos deben ser llenados.');
      return;
    }

    try {
      const serverData = {
        name: nuevoServidor.name,
        location: nuevoServidor.location,
        services: [
          {
            backend: { url: nuevoServidor.backendUrl, status: "activo" },
            frontend: { url: nuevoServidor.frontendUrl, status: "activo" },
          }
        ]
      };

      await axios.post('http://localhost:8000/api/agregar_servidor/', serverData, {  // Asegúrate que la URL apunte al backend correcto
        headers: { Authorization: `Bearer ${token}` },
      });

      setNuevoServidor({
        name: '',
        location: '',
        backendUrl: '',
        frontendUrl: '',
      });
      setMensaje('Servidor agregado exitosamente.');
      fetchServidores();
    } catch (err) {
      setError('Error al agregar el servidor.');
    }
  };

  const eliminarServidor = async (serverName) => {
    const confirmDelete = window.confirm(`¿Estás seguro de que quieres eliminar el servidor ${serverName}?`);
    if (!confirmDelete) return;

    try {
      await axios.delete(`http://localhost:8000/api/eliminar_servidor/${serverName}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchServidores();  // Recargar la lista de servidores después de eliminar
      setMensaje(`Servidor ${serverName} eliminado exitosamente.`);
    } catch (err) {
      console.error("Error al eliminar el servidor:", err);
      setError('Error al eliminar el servidor. Verifique la URL o el estado del servidor.');
    }
  };

  useEffect(() => {
    fetchServidores();
  }, [fetchServidores]);  // Ahora 'fetchServidores' está incluido como dependencia

  return (
    <div className="servidores">
      <h2>Gestión de Servidores</h2>
      <div>
        <input
          type="text"
          placeholder="Nombre del servidor"
          value={nuevoServidor.name}
          onChange={(e) => setNuevoServidor({ ...nuevoServidor, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Ubicación"
          value={nuevoServidor.location}
          onChange={(e) => setNuevoServidor({ ...nuevoServidor, location: e.target.value })}
        />
        <input
          type="url"
          placeholder="URL Backend"
          value={nuevoServidor.backendUrl}
          onChange={(e) => setNuevoServidor({ ...nuevoServidor, backendUrl: e.target.value })}
        />
        <input
          type="url"
          placeholder="URL Frontend"
          value={nuevoServidor.frontendUrl}
          onChange={(e) => setNuevoServidor({ ...nuevoServidor, frontendUrl: e.target.value })}
        />
        <button onClick={agregarServidor}>Agregar Servidor</button>
      </div>

      {error && <p className="error">{error}</p>}
      {mensaje && <p className="success">{mensaje}</p>}

      {/* Mostrar el estado general abajo del formulario */}
      <div className="status-general">
        <h3>Estado General: {statusGeneral || 'Cargando...'}</h3>
      </div>

      <ul>
        {servidores.map((servidor, index) => (
          <li key={index}>
            <h3>{servidor.name}</h3>
            <p><strong>Ubicación:</strong> {servidor.location}</p>
            <p><strong>Backend URL:</strong> {servidor.services[0].backend.url}</p>
            <p><strong>Frontend URL:</strong> {servidor.services[0].frontend.url}</p>
            <p><strong>Estado Backend:</strong> {servidor.services[0].backend.status}</p>
            <p><strong>Estado Frontend:</strong> {servidor.services[0].frontend.status}</p>
            <button className="eliminar" onClick={() => eliminarServidor(servidor.name)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Servidores;
