import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; 

const NotificationPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchNotifications = async () => {
            try {
                const token = localStorage.getItem('accessToken'); 
                const response = await axios.get('http://localhost:8000/notification', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setNotifications(response.data);
            } catch (error) {
                const errorMessage = error.response?.data?.detail || "An error occurred while fetching notifications.";
                setMessage(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
            }
        };

        fetchNotifications();
    }, []);

    return (
        <div className="notification-container">
            <h1>Notifications</h1>

            {message && <p className="error-message">{message}</p>}

            {notifications.length === 0 ? (
                <p>No notifications to display</p>
            ) : (
                <ul className="notification-list">
                    {notifications.map((notification) => (
                        <li key={notification.id} className="notification-item">
                            <p>{notification.message}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default NotificationPage;
