import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Auth from './Auth';
import HomePage from './Home';
import NotificationPage from './Notification';
import Navbar from './Navbar';

function App() {
  return (
    <Router>
      <Navbar /> 
      <Routes>
        <Route path="/" element={<Auth />} />      
        <Route path="/home" element={<HomePage />} /> 
        <Route path="/notifications" element={<NotificationPage />} />
      </Routes>
    </Router>
  );
}

export default App;
