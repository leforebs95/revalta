// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import DashboardLayout from './components/dashboard/DashboardLayout';
import LabResults from './components/dashboard/LabResults';
import LabResultDetails from './components/dashboard/LabResultDetails';
import Insights from './components/dashboard/Insights';

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
        <Route path="insights" element={<Insights />} />
        {/* Add other dashboard routes here */}
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

export default App;