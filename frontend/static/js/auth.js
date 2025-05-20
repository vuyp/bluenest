document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const messageDiv = document.getElementById('message');
    // General selector for loader, assuming one loader per auth page
    const loader = document.querySelector('.loader'); 
    const submitButton = document.querySelector('button[type="submit"]');

    const showLoader = (show) => {
        if (loader) loader.style.display = show ? 'block' : 'none';
        if (submitButton) submitButton.disabled = show;
    };

    const displayMessage = (message, type) => {
        if (messageDiv) {
            messageDiv.textContent = message;
            messageDiv.className = type; // 'success' or 'error'
        }
    };

    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            displayMessage('', ''); // Clear previous messages
            showLoader(true);
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });
                const result = await response.json();
                if (response.ok) {
                    displayMessage(`Registration successful! User ID: ${result.user.user_id}`, 'success');
                    registerForm.reset();
                    // Optionally redirect to login
                    // window.location.href = '/login'; 
                } else {
                    displayMessage(result.error || 'Registration failed.', 'error');
                }
            } catch (error) {
                console.error('Registration error:', error);
                displayMessage('An error occurred during registration.', 'error');
            } finally {
                showLoader(false);
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            displayMessage('', ''); // Clear previous messages
            showLoader(true);
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });
                const result = await response.json();
                if (response.ok) {
                    // Message displayed by redirecting page or not at all
                    localStorage.setItem('userInfo', JSON.stringify({ userId: result.user_id, email: data.email }));
                    loginForm.reset();
                    // Redirect to the main feed page
                    window.location.href = '/'; 
                    // No displayMessage here because of redirect
                } else {
                    displayMessage(result.error || 'Login failed.', 'error');
                }
            } catch (error) {
                console.error('Login error:', error);
                displayMessage('An error occurred during login.', 'error');
            } finally {
                // Hide loader only if not redirecting, but it's safer to always hide
                // if an error occurs before redirect. If redirect is immediate, this might not run.
                showLoader(false);
            }
        });
    }
});
