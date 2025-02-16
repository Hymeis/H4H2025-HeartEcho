'use client';

import { useState } from 'react';
import { useSession, signIn } from 'next-auth/react';

export default function LandingPage() {
  const { data: session, status } = useSession();
  const [isLoading, setIsLoading] = useState(false);

  if (status === 'loading' || isLoading) {
    return <p className="text-center mt-10">Loading...</p>;
  }

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-gradient-to-br from-purple-900 via-black to-gray-900 flex items-center justify-center text-center">
      {/* Decorative geometric shapes */}
      <div className="absolute bg-pink-500 w-72 h-72 rounded-full opacity-20 top-20 left-20 rotate-12" />
      <div className="absolute bg-blue-600 w-56 h-56 rounded-full opacity-20 bottom-32 right-16 rotate-45" />
      <div
        className="absolute w-full h-full mix-blend-overlay pointer-events-none bg-repeat [mask-image:radial-gradient(white,black)]"
        style={{ backgroundImage: 'url("/grid.svg")' }}
      />

      <div className="z-10 px-4 sm:px-8 max-w-2xl flex flex-col items-center">
        {/* Brand Title */}
        <h1 className="text-5xl sm:text-6xl text-white font-extrabold mb-4">
          Heart Echo
        </h1>
        {/* Subtitle */}
        <h2 className="text-xl sm:text-2xl text-white text-opacity-90 mb-6">
          Share your thoughts. Lighten your heart.
        </h2>
        {/* Paragraphs */}
        <p className="text-white text-opacity-90 mb-8 max-w-lg">
          Everyone faces moments of anxiety, stress, or daily pressures. 
          Heart Echo is your safe haven to release those burdens—anonymously. 
          Share your story, find encouragement, and know that you’re not alone.
        </p>

        {/* Sign in Button */}
        <button
          onClick={() => {
            setIsLoading(true);
            signIn('google', { callbackUrl: '/homepage' });
          }}
          className="bg-white text-black px-6 py-3 rounded-full font-semibold hover:bg-gray-200 transition"
        >
          Sign in with Google
        </button>
      </div>
    </div>
  );
}
