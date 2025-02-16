'use client';

import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import Link from 'next/link';
import { Post } from './_types';
import NavBar from './_components/NavBar';

export default function Homepage() {
  const { data: session, status } = useSession();
  const [posts, setPosts] = useState<Post[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch posts from your backend
    const fetchPosts = async () => {
      try {
        const res = await fetch('/api/posts'); // e.g. GET /api/posts
        if (!res.ok) {
          throw new Error('Failed to fetch posts');
        }
        const data = (await res.json()) as Post[];
        // Sort by timestamp descending (most recent first)
        data.sort((a, b) => b.timestamp - a.timestamp);
        setPosts(data);
      } catch (err) {
        setError((err as Error).message || 'Error fetching posts');
      }
    };

    fetchPosts();
  }, []);

  if (status === 'loading') {
    return (
      <>
        <p>Loading session...</p>
      </>
    )
  }

  if (!session) {
    return (
      <>
        <NavBar />
        <p>Log in in to view all posts</p>
      </>
    )
  }

  return (
    <div className="w-full mx-auto p-4">
      <NavBar />
      <main className='p-12'>
        <h1 className="text-2xl font-bold mb-4">Recent Posts</h1>
        {error && <p className="text-red-500">{error}</p>}
        {!error && posts.length === 0 && (
          <p>No posts yet.</p>
        )}
        {posts.map((post) => (
          <Link key={post.post_id} href={`/homepage/${post.post_id}`}>
            <div className="border rounded p-4 mb-4 hover:bg-gray-50 cursor-pointer">
              <h2 className="font-semibold">
                {post.title || '(No Title)'}
              </h2>
              <p className="text-sm text-gray-500">
                {new Date(post.timestamp).toLocaleString()}
                {` • From: ${post.random_name}`}
              </p>
              <p className="mt-2 text-gray-700 line-clamp-2 overflow-hidden">
                {post.content}
              </p>
            </div>
          </Link>
        ))}       
      </main>
    </div>
  );
}
