/**
 * Login handler for the wedding site
 * Used in Hugging Face Spaces deployment
 */

// Detect if we're running in Hugging Face Spaces
const isHuggingFace = window.location.hostname.includes('huggingface.co');

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm && isHuggingFace) {
        // Override the form action for Hugging Face
        loginForm.action = window.location.pathname;
        
        // Add client-side handling for Hugging Face
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Make a fetch request to the login endpoint
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'username': username,
                    'password': password
                }),
                credentials: 'include'
            })
            .then(response => {
                if (response.redirected) {
                    // Follow the redirect
                    window.location.href = response.url;
                } else if (response.ok) {
                    // Try to go to home page
                    window.location.href = '/home';
                } else {
                    // Show error
                    document.getElementById('error-message').style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Login error:', error);
                document.getElementById('error-message').style.display = 'block';
            });
        });
    }
});