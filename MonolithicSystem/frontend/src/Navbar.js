
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './App.css';

const Navbar = () => {
    const location = useLocation(); 

    return (
        <nav className="navbar">
            <ul>
                <li>
                    <Link to="/" className={location.pathname === '/' ? 'active' : ''}>SignIn/SignUp</Link>
                </li>
                <li>
                    <Link to="/home" className={location.pathname === '/home' ? 'active' : ''}>Home</Link>
                </li>
                <li>
                    <Link to="/notifications" className={location.pathname === '/notifications' ? 'active' : ''}>Notifications</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
