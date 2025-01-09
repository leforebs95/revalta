// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ProtectedRoute from './components/ProtectedRoute';
import { CSRFProvider } from './providers/CSRFProvider';
import { AuthProvider } from './providers/AuthProvider';

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        } 
      />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <CSRFProvider>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </CSRFProvider>
    </Router>
  );
}

export default App;