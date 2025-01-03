import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Auth from './Auth';
import HomePage from './Home';
import NotificationPage from './Notification';
import Navbar from './Navbar';

function App() {
  const isAuthenticated = localStorage.getItem('accessToken') !== null;

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route
          path="/home"
          element={isAuthenticated ? <HomePage /> : <Navigate to="/" />}
        />
        <Route
          path="/notifications"
          element={isAuthenticated ? <NotificationPage /> : <Navigate to="/" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
