document.addEventListener('DOMContentLoaded', () => {
    const createPostForm = document.getElementById('createPostForm');
    const postMessageDiv = document.getElementById('postMessage');
    const postsContainer = document.getElementById('postsContainer');
    const createPostLoader = document.getElementById('createPostLoader');
    const postsLoader = document.getElementById('postsLoader'); // Loader for the feed
    const createPostButton = createPostForm ? createPostForm.querySelector('button[type="submit"]') : null;

    const showCreatePostLoader = (show) => {
        if (createPostLoader) createPostLoader.style.display = show ? 'block' : 'none';
        if (createPostButton) createPostButton.disabled = show;
    };

    const showPostsLoader = (show) => {
        if (postsLoader) postsLoader.style.display = show ? 'block' : 'none';
    };

    const displayPostMessage = (message, type) => {
        if (postMessageDiv) {
            postMessageDiv.textContent = message;
            postMessageDiv.className = type; // 'success' or 'error'
        }
    };

    const fetchAndDisplayPosts = async () => {
        if (!postsContainer) return;
        showPostsLoader(true);
        postsContainer.innerHTML = ''; // Clear previous posts before loading

        try {
            const response = await fetch('http://localhost:5000/posts');
            if (!response.ok) {
                postsContainer.innerHTML = '<p>Error loading posts. Could not connect to server.</p>';
                console.error('Failed to fetch posts:', response.status);
                return;
            }
            const posts = await response.json();
            if (posts.length === 0) {
                postsContainer.innerHTML = '<p>No posts yet. Be the first to create one!</p>';
                return;
            }
            // postsContainer.innerHTML = ''; // Already cleared
            posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.className = 'post';
                // In a real app, user_id would be used to fetch username
                postElement.innerHTML = `
                    <h3>Post by User #${post.user_id}</h3>
                    <p>${post.content.replace(/\n/g, '<br>')}</p> 
                    <small>Post ID: ${post.post_id}</small>
                `;
                postsContainer.appendChild(postElement);
            });
        } catch (error) {
            console.error('Error fetching posts:', error);
            postsContainer.innerHTML = '<p>Error loading posts. Please try again later.</p>';
        } finally {
            showPostsLoader(false);
        }
    };

    if (createPostForm) {
        createPostForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            displayPostMessage('', ''); // Clear previous messages
            showCreatePostLoader(true);
            const content = document.getElementById('postContent').value;
            
            // Retrieve user info from localStorage
            const userInfo = JSON.parse(localStorage.getItem('userInfo'));
            let userId; 
            if (userInfo && userInfo.userId) {
                userId = userInfo.userId;
            } else {
                displayPostMessage('You must be logged in to post. Redirecting to login...', 'error');
                showCreatePostLoader(false);
                setTimeout(() => { window.location.href = '/login'; }, 2000);
                return;
            }

            if (!content.trim()) {
                displayPostMessage('Post content cannot be empty.', 'error');
                showCreatePostLoader(false);
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/posts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_id: userId, content: content }),
                });
                const result = await response.json();
                if (response.ok) {
                    displayPostMessage('Post created successfully!', 'success');
                    createPostForm.reset();
                    fetchAndDisplayPosts(); // Refresh the posts list
                } else {
                    displayPostMessage(result.error || 'Failed to create post.', 'error');
                }
            } catch (error) {
                console.error('Create post error:', error);
                displayPostMessage('An error occurred while creating the post.', 'error');
            } finally {
                showCreatePostLoader(false);
            }
        });
    }

    // Initial fetch of posts when the page loads
    // Ensure this runs only on pages with postsContainer (like index.html)
    if (postsContainer) { 
        fetchAndDisplayPosts();
    }
});
