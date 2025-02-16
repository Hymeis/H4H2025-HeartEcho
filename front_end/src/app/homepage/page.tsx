'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import NavBar from './_components/NavBar';
import WritePost from './_components/WritePost';

type Post = {
  pid: string;
  user_id: string;
  title: string;
  content: string;
  tag: string;
  user_nickname: string;
  likes: number;
  comment_list: string[];
  timestamp: string; // or Date if you parse it
};

export default function Homepage() {
  const router = useRouter();
  const { data: session, status } = useSession();

  // **Posts** state (fetched from backend)
  const [posts, setPosts] = useState<Post[]>([]);
  // **Modal** open/close
  const [isModalOpen, setModalOpen] = useState(false);

  // If session is loading, show a placeholder
  if (status === 'loading') {
    return <p>Loading session...</p>;
  }

  // If no session, redirect to /login (or handle however you prefer)
  useEffect(() => {
    if (!session && status !== 'loading') {
      router.push('/login');
    }
  }, [session, status, router]);

  // ==========================
  // Fetch the latest 10 posts
  // ==========================
  async function fetchLatestPosts() {
    try {
      const res = await fetch('/posts/by_time', {
        method: 'GET',
      });
      if (!res.ok) {
        throw new Error('Failed to fetch posts');
      }
      const data = await res.json();
      setPosts(data.posts || []);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  }

  // Fetch posts once when logged in
  useEffect(() => {
    if (session) {
      fetchLatestPosts();
    }
  }, [session]);

  // Handle "Add Post" button in NavBar
  const handleAddPostClick = () => {
    setModalOpen(true);
  };
  // Close modal
  const closeModal = () => {
    setModalOpen(false);
  };

  // Callback to re-fetch posts after creating a new one
  const handlePostCreated = async () => {
    await fetchLatestPosts();
    setModalOpen(false); // close modal
  };

  return (
    <div className="bg-black min-h-screen text-white">
      {/* Pass callback to NavBar */}
      <NavBar onAddPostClick={handleAddPostClick} />

      <section className="max-w-3xl mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Latest Posts</h1>

        {/* Display the 10 posts sorted by timestamp (already sorted by backend) */}
        {posts.length === 0 ? (
          <p>No posts yet.</p>
        ) : (
          posts.map((post) => (
            <div
              key={post.pid}
              className="border-b border-gray-700 py-4 mb-4 last:mb-0 last:border-none"
            >
              <h2 className="text-xl font-semibold mb-1">
                {post.title || '(No Title)'}
              </h2>
              <p className="text-sm text-gray-400 mb-2">
                By {post.user_nickname} • {new Date(post.timestamp).toLocaleString()}
              </p>
              <p className="text-white mb-2">{post.content}</p>
              <p className="text-sm text-gray-500">
                Tag: {post.tag} | Likes: {post.likes}
              </p>
            </div>
          ))
        )}
      </section>

      {/* Conditionally render the modal for writing a new post */}
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

            {/* Pass callback to <WritePost /> so it can trigger re-fetch */}
            <WritePost
              onPostCreated={handlePostCreated}
              userId={session?.user?.uid || 'unknown'}
            />
          </div>
        </div>
      )}
    </div>
  );
}
