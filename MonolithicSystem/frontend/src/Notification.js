import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Assuming you have a CSS file for styling

const NotificationPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [message, setMessage] = useState('');

    // Fetch notifications when the component mounts
    useEffect(() => {
        const fetchNotifications = async () => {
            try {
                const token = localStorage.getItem('accessToken'); // Get token from localStorage
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
                            {/* You can add more fields if needed */}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default NotificationPage;
