import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';  // Assuming you are using the same CSS file for styling

const HomePage = () => {
    const [posts, setPosts] = useState([]);
    const [content, setContent] = useState('');
    const [codeFile, setCodeFile] = useState(null);
    const [message, setMessage] = useState('');

    // Fetch the posts when the component mounts
    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const token = localStorage.getItem('accessToken');  // Get token from localStorage
                const response = await axios.get('http://localhost:8000/post', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                const postsData = response.data;

                // Backend already provides code snippets if they exist
                setPosts(postsData);
            } catch (error) {
                const errorMessage = error.response?.data?.detail || "An error occurred";
                setMessage(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
            }
        };

        fetchPosts();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('accessToken');
        const formData = new FormData();
        formData.append('content', content);
        if (codeFile) {
            formData.append('codeFile', codeFile);
        }

        try {
            const response = await axios.post('http://localhost:8000/post', formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            setMessage('Post created successfully');
            setContent('');  // Clear content input
            setCodeFile(null);  // Clear file input
            // setPosts([response.data, ...posts]);  // Add new post to the beginning of the posts list
        } catch (error) {
            const errorMessage = error.response?.data?.detail || "An error occurred";
            setMessage(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
        }
    };

    return (
        <div className="home-container">
            <h1>Home Page - Posts</h1>

            <div className="create-post">
                <form onSubmit={handleSubmit}>
                    <textarea
                        placeholder="What's on your mind?"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                        className="post-input"
                    />
                    <input
                        type="file"
                        onChange={(e) => setCodeFile(e.target.files[0])}
                        className="file-input"
                    />
                    <button type="submit" className="post-button">Create Post</button>
                </form>
                {message && <p className="message">{message}</p>}
            </div>

            <div className="posts-list">
                {posts.length === 0 ? (
                    <p>No posts to display</p>
                ) : (
                    posts.map((post) => (
                        <div key={post.id} className="post">
                            <p>{post.content}</p>
                            {post.codeFile && post.codeFile.length > 0 && (
                                <pre className="code-snippet">
                                    <code>{post.codeFile}</code> {/* Displaying code content */}
                                </pre>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default HomePage;
