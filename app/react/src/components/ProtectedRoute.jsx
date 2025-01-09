import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../providers/AuthProvider';

export function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div>Loading...</div>; // Consider replacing with a proper loading component
  }

  if (!user) {
    // Redirect to login but save the attempted url
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

export default ProtectedRoute;