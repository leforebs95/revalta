import React from "react";

interface AuthLayoutProps {
    children: React.ReactNode;
    title: string;
    subtitle?: string;
  }
  
  export const AuthLayout = ({ children, title, subtitle }: AuthLayoutProps) => {
    return (
      <div className="flex min-h-screen">
        <div className="flex flex-1 flex-col justify-center px-4 py-12 sm:px-6 lg:flex-none lg:px-20">
          <div className="mx-auto w-full max-w-sm lg:w-96">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900">{title}</h2>
              {subtitle && (
                <p className="mt-2 text-sm text-gray-600">{subtitle}</p>
              )}
            </div>
            <div className="mt-8">{children}</div>
          </div>
        </div>
        <div className="relative hidden w-0 flex-1 lg:block">
          <img
            className="absolute inset-0 h-full w-full object-cover"
            src="/images/auth-background.jpg"
            alt="Authentication background"
          />
        </div>
      </div>
    );
  };