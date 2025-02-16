'use client';

import React from 'react';
import { signIn, signOut, useSession } from 'next-auth/react';

export default function NavBar() {
  const { data: session, status } = useSession();
  const isLoading = status === 'loading';

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <nav className="flex items-center justify-between bg-white py-4 px-6 shadow">
      <div className="text-xl font-bold">Hack For Humanity 2025</div>
      <div>
        {session ? (
          <button
            onClick={() => signOut({ callbackUrl: '/homepage' })}
            className="text-gray-700 hover:text-gray-900"
          >
            Log out
          </button>
        ) : (
          <button
            onClick={() => signIn('google', { callbackUrl: '/homepage' })}
            className="text-gray-700 hover:text-gray-900"
          >
            Log in
          </button>
        )}
      </div>
    </nav>
  );
}
