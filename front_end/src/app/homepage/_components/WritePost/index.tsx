'use client';
import React, { useState } from 'react';

interface WritePostProps {
  onPostCreated: () => void;
  userId: string;
}

export default function WritePost({ onPostCreated, userId }: WritePostProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tag, setTag] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const response = await fetch('/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          title,
          content,
          tag,
        }),
      });
      if (!response.ok) {
        throw new Error(`Failed to submit post. Code: ${response.status}`);
      }
      const data = await response.json();
      console.log('Post created:', data);

      // Clear fields
      setTitle('');
      setContent('');
      setTag('');

      // Parent callback to refresh posts
      onPostCreated();
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block font-medium">Title</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border p-2 rounded"
          placeholder="Optional title"
        />
      </div>
      <div>
        <label className="block font-medium">Content</label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full border p-2 rounded"
          rows={5}
          placeholder="Share your thoughts..."
          required
        />
      </div>
      <div>
        <label className="block font-medium">Tag</label>
        <input
          type="text"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
          className="w-full border p-2 rounded"
          placeholder="E.g., stress, anxiety, daily-life"
        />
      </div>
      {error && <p className="text-red-500">{error}</p>}
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Submitting...' : 'Add Post'}
      </button>
    </form>
  );
}
