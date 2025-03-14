import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import hero from '../assets/images/hero.svg';
import Login from '../components/login/LoginCard';
import { useAuth } from '../hooks/useAuth';

const LoginPage = () => {
  const navigate = useNavigate();
  // const { csrfToken, loading: csrfLoading } = useCSRF();
  const { user, isLoading } = useAuth();
  
  // Redirect if user is already logged in
  useEffect(() => {
    if (!isLoading && user) {
      navigate('/dashboard');
    }
  }, [user, navigate, isLoading]);


  const handleLogoClick = () => {
    navigate('/');
  };

  return (
    <>
      <header className="absolute">
        <button 
          className="mt-10 mb-10 ml-10 col-span-1 text-whisper font-sans font-bold text-4xl"
          onClick={handleLogoClick}
        >
          Nivalta
        </button>
      </header>

      <main className="flex justify-center items-center mx-auto gap-52 border border-black h-screen">
        <div className="flex items-center align-middle justify-center h-auto flex-wrap w-[500px]">
          <img 
            src={hero} 
            alt="logo" 
            className="mb-20"
          />
          <p className="text-white font-sans text-2xl text-wrap text-center">
            Discover the power of personalized health insights and seamless tracking with Nivalta.
          </p>
        </div>
        <div className="rounded-lg">
          <Login/>
        </div>
      </main>
    </>
  );
};

export default LoginPage;