import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; 
import './App.css';  

const Auth = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSignUp, setIsSignUp] = useState(true);
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = isSignUp ? 'http://localhost:8000/auth/signup' : 'http://localhost:8000/auth/signin';
        const payload = { email, password };
        try {
            const response = await axios.post(url, payload);
            if (isSignUp) {
                setMessage("User created successfully");
            } else {
                localStorage.setItem('accessToken', response.data.accessToken);
                setMessage("Signed in successfully");
                
                navigate('/home');            }
        } catch (error) {
            const errorMessage = error.response?.data?.detail || "An error occurred";
            setMessage(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <h1>{isSignUp ? 'Sign Up' : 'Sign In'}</h1>
                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="auth-input"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="auth-input"
                    />
                    <button type="submit" className="auth-button">{isSignUp ? 'Sign Up' : 'Sign In'}</button>
                </form>
                <button onClick={() => setIsSignUp(!isSignUp)} className="switch-button">
                    Switch to {isSignUp ? 'Sign In' : 'Sign Up'}
                </button>
                {message && <p className="auth-message">{message}</p>}
            </div>
        </div>
    );
};

export default Auth;
