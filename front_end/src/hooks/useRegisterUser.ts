'use client';

import { useEffect } from 'react';
import { useSession } from 'next-auth/react';

export function useRegisterUser() {
  const { data: session, status } = useSession();

  useEffect(() => {
    if (status === 'authenticated' && session?.user?.email) {
      fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: session.user.email }),
      })
        .then((res) => res.json())
        .then((data) => console.log('Registration result:', data))
        .catch((err) => console.error('Registration error:', err));
    }
  }, [session, status]);
}