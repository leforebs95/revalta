import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Login from '../components/login/LoginCard';

const LoginPage = () => {
  const navigate = useNavigate();
  
  // We'll need to fetch these from your API or context
  const [csrfToken, setCsrfToken] = React.useState(null);
  const [session, setSession] = React.useState({ login: false });

  // Fetch initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        // Replace these with your actual API endpoints
        const [sessionRes, csrfRes] = await Promise.all([
          fetch('/api/session'),
          fetch('/api/csrf-token')
        ]);
        
        const sessionData = await sessionRes.json();
        const csrfData = await csrfRes.json();
        
        setSession(sessionData);
        setCsrfToken(csrfData.csrfToken);
      } catch (error) {
        console.error('Error fetching initial data:', error);
      }
    };

    fetchInitialData();
  }, []);

  // Redirect if logged in
  useEffect(() => {
    if (session.login) {
      navigate('/dashboard');
    }
  }, [session.login, navigate]);

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
            src="/images/hero.svg" 
            alt="logo" 
            className="mb-20"
          />
          <p className="text-white font-sans text-2xl text-wrap text-center">
            Discover the power of personalized health insights and seamless tracking with Nivalta.
          </p>
        </div>
        <div className="rounded-lg">
          <Login csrfToken={csrfToken} />
        </div>
      </main>
    </>
  );
};

export default LoginPage;