'use client';

import React from 'react';
import { signIn, signOut, useSession } from 'next-auth/react';
import Link from 'next/link';

interface NavBarProps {
  onAddPostClick?: () => void;
}

export default function NavBar({ onAddPostClick }: NavBarProps) {
  const { data: session, status } = useSession();
  const isLoading = status === 'loading';

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <nav className="flex items-center justify-between bg-black py-4 px-6 shadow">
      <div className="text-xl font-bold text-white">Heart Echo</div>

      <div className="flex items-center space-x-6">
        {/* Add link to /chat */}
        <Link href="/chat" className="text-white hover:text-gray-300">
          Chat
        </Link>

        {session ? (
          <>
            {onAddPostClick && (
              <button
                onClick={onAddPostClick}
                className="text-white hover:text-gray-300"
              >
                + Add Post
              </button>
            )}
            <button
              onClick={() => signOut({ callbackUrl: '/homepage' })}
              className="text-white hover:text-gray-300"
            >
              Log out
            </button>
          </>
        ) : (
          <button
            onClick={() => signIn('google', { callbackUrl: '/homepage' })}
            className="text-white hover:text-gray-300"
          >
            Log in
          </button>
        )}
      </div>
    </nav>
  );
}
