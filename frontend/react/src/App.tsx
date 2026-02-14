import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import { LoginForm } from './components/LoginForm/LoginForm';
import { RegisterForm } from './components/RegisterForm/RegisterForm';
import { Home } from './pages/Home';


export const API_URL = "http://localhost/api/livres/";
export const isAdmin = true;

function App() {

  return (
    <Router>
      <Routes>
        {/* Par défaut, on va sur la recherche */}
        <Route path="/" element={<Home />} />

        {/* Route pour le login */}
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />

        {/* Redirection si l'URL n'existe pas */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  )
}

export default App
