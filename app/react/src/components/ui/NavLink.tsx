import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function NavLink({ to, children, className }) {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link
      to={to}
      className={`${className} ${
        isActive ? 'bg-nivaltaBlue text-white' : 'text-[#202020]'
      } w-[146px] py-2 rounded-[40px] flex items-center gap-3 px-3 transition-colors`}
    >
      {children}
    </Link>
  );
}

export default NavLink;