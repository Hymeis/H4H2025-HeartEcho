export type Post = {
    post_id: string;
    uid: string;
    title?: string;
    content: string;
    timestamp: number;
    num_likes: number;
    tag: string;
    comment_list: string[];
    random_name: string;
}

export type User = {
    uid: string;
    email: string;
    post_list: string[];
    like_list: string[];
}

export type Comment = {
    comment_id: string;
    post_id: string;
    uid: string;
    comment_content: string;
    timestamp: number;
    num_likes: number;
    comment_from: string;
}