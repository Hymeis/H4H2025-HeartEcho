'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import NavBar from './_components/NavBar';
import WritePost from './_components/WritePost';

export default function Homepage() {
  const router = useRouter();
  const { data: session, status } = useSession();

  // Modal open state
  const [isModalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    if (!session && status !== 'loading') {
      router.push('/');
    }
  }, [session, status, router]);

  if (status === 'loading') {
    return <p>Loading session...</p>;
  }

  // Callback for NavBar
  const handleAddPostClick = () => {
    setModalOpen(true);
  };

  // Close modal callback
  const closeModal = () => {
    setModalOpen(false);
  };

  return (
    <div className="bg-black min-h-screen text-white">
      {/* Pass the callback down */}
      <NavBar onAddPostClick={handleAddPostClick} />

      <section className="max-w-3xl mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">
          Welcome to Our Anonymous Thoughts Board!
        </h1>
        {/* Other homepage content here (posts list, etc.) */}
      </section>

      {/* Conditionally render the modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          {/* Overlay background */}
          <div
            className="absolute inset-0 bg-black bg-opacity-50"
            onClick={closeModal}
          />
          {/* Modal content */}
          <div className="relative bg-white text-black p-6 rounded shadow-lg w-full max-w-2xl mx-auto">
            <button
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
              onClick={closeModal}
            >
              Close ✕
            </button>

            {/* WritePost form inside the modal */}
            <WritePost />
          </div>
        </div>
      )}
    </div>
  );
}
