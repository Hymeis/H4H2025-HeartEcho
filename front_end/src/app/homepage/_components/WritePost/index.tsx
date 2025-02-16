'use client';

import React, { useState } from 'react';
import { useSession } from 'next-auth/react';

const TAG_OPTIONS = [
  { value: 'positive', label: 'Positive' },
  { value: 'neutral', label: 'Neutral' },
  { value: 'negative', label: 'Negative' },
];

export default function WritePost() {
  const { data: session } = useSession();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tag, setTag] = useState('');
  const [photos, setPhotos] = useState<File[]>([]);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files);
      if (filesArray.length > 9) {
        setError('Maximum 9 photos are allowed.');
        return;
      }
      setPhotos(filesArray);
      setError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    
    try {
      const uid = session?.user?.uid;
      if (!uid) {
        throw new Error('User UID not found');
      }
      const postPayload = {
        uid,
        title,
        content,
        timestamp: Date.now(),
        tag,
      };

      let response;
      if (photos.length > 0) {
        // Use FormData when photos are included
        const formData = new FormData();
        formData.append('uid', uid);
        formData.append('title', title);
        formData.append('content', content);
        formData.append('timestamp', Date.now().toString());
        formData.append('tag', tag);
        photos.forEach((file, index) => {
          formData.append(`photo_${index}`, file);
        });
        response = await fetch('/post', {
          method: 'POST',
          body: formData,
        });
      } else {
        // Send as JSON if no photos
        response = await fetch('/post', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(postPayload),
        });
      }
      if (!response.ok) {
        throw new Error('Failed to submit post');
      }
      // Clear fields after success
      setTitle('');
      setContent('');
      setTag('');
      setPhotos([]);
      alert('Post submitted successfully');
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-4 space-y-4">
      <div>
        <label className="block font-medium">Title (optional)</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border p-2 rounded"
          placeholder="Enter your title"
        />
      </div>
      <div>
        <label className="block font-medium">Content</label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full border p-2 rounded"
          rows={6}
          placeholder="Write your post here..."
          required
        ></textarea>
      </div>
      <div>
        <label className="block font-medium">Tag (optional)</label>
        <select
          value={tag}
          onChange={(e) => setTag(e.target.value)}
          className="w-full border p-2 rounded"
        >
          <option value="">Select a tag</option>
          {TAG_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label className="block font-medium">Photos (max 9)</label>
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileChange}
          className="w-full"
        />
        {photos.length > 0 && (
          <p className="mt-1 text-sm text-gray-600">{photos.length} photo(s) selected</p>
        )}
      </div>
      {error && <p className="text-red-500">{error}</p>}
      <div>
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Submitting...' : 'Finish'}
        </button>
      </div>
    </form>
  );
}
