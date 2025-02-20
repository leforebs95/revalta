// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import DashboardLayout from './components/dashboard/DashboardLayout';
import LabResults from './components/dashboard/LabResults';
import LabResultDetails from './components/dashboard/LabResultDetails';
import { CSRFProvider } from './providers/CSRFProvider';
import { AuthProvider } from './providers/AuthProvider';

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<DashboardLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="lab-results" element={<LabResults />} />
        <Route path="lab-results/:docId" element={<LabResultDetails />} />
        {/* Add other dashboard routes here */}
      </Route>
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