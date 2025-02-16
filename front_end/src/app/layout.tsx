'use client';
import { useState, useEffect } from 'react';
import LoadingScreen from '@/components/LoadingScreen'; 
import './globals.css';
import Providers from './providers';
import NavBar from './homepage/_components/NavBar';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading. In real usage, check if essential data or images are ready.
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <html lang="en">
      <body>
        <Providers>
          {isLoading ? <LoadingScreen /> : children}
        </Providers>
      </body>
    </html>
  );
}
