// src/app/(auth)/login/page.tsx
'use client';

import { useEffect } from 'react';
import { signIn, useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const { data: session, status } = useSession();

  useEffect(() => {
    if (session) {
      router.push('/homepage');
    }
  }, [session, router]);

  if (status === 'loading') return <p>Loading...</p>;

  if (session) {
    // Optionally, you can render nothing or a loading indicator while redirecting.
    return null;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        onClick={() => signIn('google', { callbackUrl: '/homepage' })}
      >
        Sign in with Google
      </button>
    </div>
  );
}
