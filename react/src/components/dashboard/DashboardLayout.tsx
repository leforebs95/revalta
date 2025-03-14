import logoSrc from '../../assets/images/nivalta-logo.svg';
import folderIcon from '../../assets/images/vuesax-linear-open-folder.svg';
import peopleIcon from '../../assets/images/vuesax-linear-people.svg';
import settingIcon from '../../assets/images/vuesax-linear-setting2.svg';
import directInboxIcon from '../../assets/images/vuesax-linear-direct-inbox.svg';
import taskSquareIcon from '../../assets/images/vuesax-linear-task-square.svg';
import logoutIcon from '../../assets/images/vuesax-linear-logout.svg';
import React, { useEffect } from 'react';
import { useNavigate, Link, Outlet } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface NavItemProps {
  to: string;
  icon: string;
  text: string;
}

const DashboardLayout = () => {
  const navigate = useNavigate();
  const { user, isLoading, logout } = useAuth();

  // Protect route
  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login');
    }
  }, [user, navigate, isLoading]);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Error logging out', error);
    }
  };

  return (
    <div className="relative bg-white rounded-lg w-full min-h-screen">
      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 min-h-screen bg-white border-r">
          {/* Logo */}
          <div className="h-40 flex items-center justify-center">
            <img 
              src={logoSrc}
              alt="Nivalta Company Logo" 
              className="w-32"
            />
          </div>

          {/* Navigation Menu */}
          <div className="px-6 py-4">
            <div className="mb-4">
              <h2 className="text-[#3f3f3f] text-base font-semibold font-['Poppins'] uppercase">Overview</h2>
            </div>

            <nav className="space-y-2">
              <NavItem 
                to="/dashboard"
                icon={directInboxIcon}
                text="Dashboard"
              />
              <NavItem 
                to="/dashboard/symptoms"
                icon={folderIcon}
                text="Symptom Log"
              />
              <NavItem 
                to="/dashboard/lab-results"
                icon={taskSquareIcon}
                text="Lab Results"
              />
              <NavItem 
                to="/dashboard/family-history"
                icon={peopleIcon}
                text="Family History"
              />
              <NavItem 
                to="/dashboard/insights"
                icon={settingIcon}
                text="Insights"
              />
            </nav>

            {/* Settings Section */}
            <div className="absolute bottom-0 left-0 w-64 p-6 border-t">
              <div className="mb-4">
                <h2 className="text-[#3f3f3f] text-base font-semibold font-['Poppins'] uppercase">Settings</h2>
              </div>
              
              <NavItem 
                to="/dashboard/settings"
                icon={settingIcon}
                text="Settings"
              />
              
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-3 py-2 px-4 text-red-500 hover:bg-red-50 rounded-full transition-colors"
              >
                <img 
                  src={logoutIcon}
                  alt="Logout icon" 
                  className="w-4 h-4"
                />
                <span className="font-medium">Logout</span>
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-8">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

const NavItem = ({ to, icon, text }: NavItemProps) => (
  <Link
    to={to}
    className="flex items-center gap-3 py-2 px-4 text-gray-800 hover:bg-gray-100 rounded-full transition-colors"
  >
    <img src={icon} alt={`${text} icon`} className="w-4 h-4" />
    <span className="font-medium">{text}</span>
  </Link>
);

export default DashboardLayout;