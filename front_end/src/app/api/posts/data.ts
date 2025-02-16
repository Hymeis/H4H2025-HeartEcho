import { Post } from '@/app/homepage/_types';

let mockPosts: Post[] = [
  {
    post_id: 'p1',
    uid: 'mockuser1',
    title: 'Hello Santa Clara!',
    content: 'This is my first post. Excited to share!',
    timestamp: Date.now() - 60 * 60 * 1000, // 1 hour ago
    num_likes: 0,
    tag: 'positive',
    comment_list: [],
    random_name: 'AnonymousBronco',
  },
  {
    post_id: 'p2',
    uid: 'mockuser2',
    title: 'Exams Coming Up',
    content:
      'Feeling stressed about finals. Anyone have good study tips?',
    timestamp: Date.now() - 30 * 60 * 1000, // 30 minutes ago
    num_likes: 0,
    tag: 'neutral',
    comment_list: [],
    random_name: 'SecretScholar',
  },
];

// GET all posts
export function getAllPosts(): Post[] {
  return [...mockPosts].sort((a, b) => b.timestamp - a.timestamp);
}

// GET post by id
export function getPostById(id: string): Post | undefined {
  return mockPosts.find((p) => p.post_id === id);
}

// Create a new post
export function addPost(newPost: Post) {
  mockPosts.push(newPost);
}
