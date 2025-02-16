import { notFound } from 'next/navigation';
import { Post } from '../_types';

export default async function SinglePostPage({ params }: { params: { postId: string } }) {
  const { postId } = params;

  // GET /api/posts/[postId] or something similar
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/posts/${postId}`, {
    // to refetch
    cache: 'no-store',
  });

  if (!res.ok) {
    return notFound();
  }

  const post: Post = await res.json();

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-2">{post.title || '(No Title)'}</h1>
      <p className="mb-4 text-gray-600">By {post.random_name} &bull; {new Date(post.timestamp).toLocaleString()}</p>
      <div className="whitespace-pre-wrap">{post.content}</div>
    </div>
  );
}
