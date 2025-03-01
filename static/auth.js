
// Simple password protection for static site
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (username === '' && password === '') {
                // Set session storage to remember logged in status
                sessionStorage.setItem('authenticated', 'true');
                // Hard-code the repository-specific base URL
                window.location.href = '/wedding-site/home/';
            } else {
                document.querySelector('.error-message').textContent = 'Invalid username or password';
                document.querySelector('.error-message').style.display = 'block';
            }
        });
    }
    
    // Check if user is authenticated for protected pages
    const isHomePage = window.location.pathname.includes('/home');
    if (isHomePage && sessionStorage.getItem('authenticated') !== 'true') {
        // Hard-code the repository-specific base URL
        window.location.href = '/wedding-site/';
    }
    
    // Add logout functionality
    const logoutLink = document.createElement('a');
    logoutLink.href = '#';
    logoutLink.textContent = 'Logout';
    logoutLink.style.cssText = 'position: absolute; top: 10px; right: 20px; color: #5c8d89;';
    logoutLink.addEventListener('click', function(e) {
        e.preventDefault();
        sessionStorage.removeItem('authenticated');
        // Hard-code the repository-specific base URL
        window.location.href = '/wedding-site/';
    });
    
    if (isHomePage) {
        document.body.appendChild(logoutLink);
    }
});
