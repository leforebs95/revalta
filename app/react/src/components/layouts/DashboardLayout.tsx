import React from 'react';
import { Outlet, useNavigate, Link } from 'react-router-dom';
import { NavLink } from '../ui/NavLink';

function DashboardLayout() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await fetch('/api/logout');
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="DashboardLeftNav w-full h-screen relative bg-white rounded-[10px]">
      <img
        className="Nivalta13 w-[173px] h-[173px] left-[26px] top-[-24px] absolute"
        src="/images/nivalta-logo.svg"
        alt="Nivalta Company Logo"
      />
      
      <div className="Frame10 w-[216px] h-[337px] left-[41px] top-[149px] absolute flex-col justify-start items-start gap-2.5 inline-flex">
        <div className="Frame11 w-[146px] py-2 justify-start items-center gap-2.5 inline-flex">
          <div className="Overview grow shrink basis-0 text-[#3f3f3f] text-base font-semibold uppercase">
            OVERVIEW
          </div>
        </div>
        <nav className="Frame17 flex-col justify-center items-center gap-2 flex">
          <NavLink to="/dashboard" className="nav-link">
            <img src="/images/vuesax-linear-direct-inbox.svg" alt="Dashboard" />
            <span>Dashboard</span>
          </NavLink>
          
          <NavLink to="/dashboard/symptoms" className="nav-link">
            <img src="/images/vuesax-linear-open-folder.svg" alt="Symptoms" />
            <span>Symptom Log</span>
          </NavLink>
          
          <NavLink to="/dashboard/lab-results" className="nav-link">
            <img src="/images/vuesax-linear-task-square.svg" alt="Lab Results" />
            <span>Lab Results</span>
          </NavLink>
          
          {/* Additional navigation items */}
        </nav>
      </div>
      
      <div className="Frame12 h-[140px] left-[40px] bottom-[20px] absolute flex-col justify-start items-start gap-2.5 inline-flex">
        <button
          onClick={handleLogout}
          className="Btn self-stretch py-2 rounded-[40px] justify-start items-center gap-3 inline-flex text-[#f13e3e]"
        >
          <img src="/images/vuesax-linear-logout.svg" alt="Logout" />
          <span>Logout</span>
        </button>
      </div>
      
      <main className="ml-[260px] p-6">
        <Outlet />
      </main>
    </div>
  );
}