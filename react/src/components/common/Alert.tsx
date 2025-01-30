import React from 'react';
import { AlertCircle } from 'lucide-react';

interface AlertProps {
  children: React.ReactNode;
  variant?: 'default' | 'destructive';
}

export const Alert: React.FC<AlertProps> = ({ children, variant = 'default' }) => {
  const baseStyles = "relative w-full rounded-lg border p-4 flex items-start gap-3";
  const variantStyles = {
    default: "bg-white border-gray-200 text-gray-900",
    destructive: "bg-red-50 border-red-200 text-red-900"
  };

  return (
    <div role="alert" className={`${baseStyles} ${variantStyles[variant]}`}>
      <AlertCircle className="h-5 w-5" />
      <div className="text-sm">{children}</div>
    </div>
  );
};

export const AlertDescription = ({ children }: { children: React.ReactNode }) => (
  <div className="text-sm">{children}</div>
);