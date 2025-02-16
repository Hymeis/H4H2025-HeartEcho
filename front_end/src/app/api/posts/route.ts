import { NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';
import { getAllPosts, addPost } from './data';
import { Post } from '@/app/homepage/_types';

// GET /api/posts
export async function GET() {
  const posts = getAllPosts();
  return NextResponse.json(posts, { status: 200 });
}

// POST /api/posts
export async function POST(req: Request) {
  try {
    const json = await req.json();
    const { uid, title, content, timestamp, tag } = json;
    const newPost: Post = {
      post_id: uuidv4(),     
      uid,
      title,
      content,
      timestamp,
      tag: tag || '',
      num_likes: 0,
      comment_list: [],
      random_name: 'AnonymousUser' + Math.floor(Math.random() * 1000),
    };

    addPost(newPost);

    return NextResponse.json({ message: 'Post created', post_id: newPost.post_id }, { status: 201 });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Failed to create post' }, { status: 400 });
  }
}
