import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const NotificationPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [message, setMessage] = useState('');

    const fetchNotifications = async () => {
        try {
            const token = localStorage.getItem('accessToken');
            const response = await axios.get('http://localhost:8000/notification', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            setNotifications(response.data.reverse());
        } catch (error) {
            const errorMessage = error.response?.data?.detail || "An error occurred while fetching notifications.";
            setMessage(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
        }
    };

    const markAsSeen = async (notificationId) => {
        try {
            const token = localStorage.getItem('accessToken');
            await axios.put(`http://localhost:8000/notification/${notificationId}/mark_seen`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setNotifications((prevNotifications) =>
                prevNotifications.map((notification) =>
                    notification.id === notificationId ? { ...notification, seen: true } : notification
                )
            );
        } catch (error) {
            console.error("Error marking notification as seen:", error);
        }
    };

    useEffect(() => {
        fetchNotifications();
    }, []);

    const handleNotificationClick = (notificationId) => {
        markAsSeen(notificationId);
    };

    return (
        <div className="notification-container">
            <h1>Notifications</h1>

            {message && <p className="error-message">{message}</p>}

            {notifications.length === 0 ? (
                <p>No notifications to display</p>
            ) : (
                <ul className="notification-list">
                    {notifications.map((notification) => (
                        <li
                            key={notification.id}
                            className={`notification-item ${notification.seen ? 'seen' : 'unseen'}`}
                            onClick={() => handleNotificationClick(notification.id)}
                        >
                            <p>{notification.message}</p>
                            <p className="notification-timestamp">
                                {new Date(notification.createdAt).toLocaleString()}
                            </p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default NotificationPage;
