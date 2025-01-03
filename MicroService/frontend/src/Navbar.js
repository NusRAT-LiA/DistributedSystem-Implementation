import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './App.css';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = localStorage.getItem('accessToken') !== null;

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/');
  };

  return (
    <nav className="navbar">
      <ul>
        {!isAuthenticated ? (
          <li>
            <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Sign In/Sign Up</Link>
          </li>
        ) : (
          <>
            <li>
              <Link to="/home" className={location.pathname === '/home' ? 'active' : ''}>Home</Link>
            </li>
            <li>
              <Link to="/notifications" className={location.pathname === '/notifications' ? 'active' : ''}>Notifications</Link>
            </li>
            <li>
              <button onClick={handleLogout} className="logout-button">Logout</button>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
