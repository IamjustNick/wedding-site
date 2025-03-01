
// Simple password protection for static site
document.addEventListener('DOMContentLoaded', function() {
    console.log('Auth script loaded!');
    
    // Login page handling
    if (document.getElementById('login-form')) {
        document.getElementById('login-form').addEventListener('submit', function(e) {
            console.log('Form submitted');
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            console.log('Checking credentials...');
            
            if (username === '' && password === '') {
                console.log('Login successful');
                sessionStorage.setItem('authenticated', 'true');
                window.location.href = '/wedding-site/home/';
            } else {
                console.log('Login failed');
                document.getElementById('error-message').style.display = 'block';
            }
        });

        // Also handle button click
        document.getElementById('login-button').addEventListener('click', function() {
            console.log('Login button clicked');
            document.getElementById('login-form').dispatchEvent(new Event('submit'));
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
