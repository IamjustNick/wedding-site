#!/usr/bin/env python
"""
Script to generate static files for GitHub Pages deployment.
This script creates a password-protected static version of the wedding site.
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

import markdown2
from jinja2 import Environment, FileSystemLoader

# Load environment variables
load_dotenv()

# Configuration
OUTPUT_DIR = Path("./site")
STATIC_DIR = Path("./app/static")
TEMPLATES_DIR = Path("./app/templates")
# Use different env var names to avoid conflicts with system USERNAME
USERNAME = os.getenv("USERNAME", "wedding")
PASSWORD = os.getenv("PASSWORD", "guest")
# For GitHub Pages, we need to know the repository name
REPO_NAME = "wedding-site"
BASE_URL = f"/{REPO_NAME}"

# Create output directory structure
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR / "static", exist_ok=True)
os.makedirs(OUTPUT_DIR / "home", exist_ok=True)

# Create .nojekyll file (prevents GitHub Pages from using Jekyll)
with open(OUTPUT_DIR / ".nojekyll", "w") as f:
    pass

# Copy static files
print("Copying static files...")
shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static", dirs_exist_ok=True)

# Load Jinja2 templates
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


# Load markdown content
def load_markdown_content(language="en"):
    if language == "es":
        markdown_file = Path("markdown_content_es.md")
    else:
        markdown_file = Path("markdown_content_en.md")

    with open(markdown_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_content, extras=["tables", "fenced-code-blocks", "break-on-newline"]
    )

    # Fix image paths
    html_content = html_content.replace("![[", f'<img src="{BASE_URL}/static/images/')
    html_content = html_content.replace("]]", '">')

    return html_content


# Helper function to add base path to static references
def process_html_for_github_pages(html_content):
    # Replace all references to /static with /wedding-site/static
    html_content = html_content.replace('href="/static', 'href="/wedding-site/static')
    html_content = html_content.replace('src="/static', 'src="/wedding-site/static')
    return html_content

# Generate login page
print("Generating login page...")
login_template = env.get_template("login.html")
login_html = login_template.render(current_year=datetime.now().year)
# Fix paths for GitHub Pages
login_html = login_html.replace('href="static/', f'href="{BASE_URL}/static/')
with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(login_html)

# Create a simple README in the site root that forwards to index.html
with open(OUTPUT_DIR / "README.md", "w", encoding="utf-8") as f:
    f.write(f"# Wedding Site\n\nPlease visit the [wedding site]({BASE_URL}/index.html) to view the content.")

# Generate home pages (EN and ES)
print("Generating home pages...")
home_template = env.get_template("home.html")

# English version
en_content = load_markdown_content("en")
en_html = home_template.render(
    content=en_content,
    lang="en",
    app_name="Wedding Site",
    current_year=datetime.now().year,
    url_for=lambda name, **kwargs: f"{BASE_URL}/{name}"
    + (f"/{kwargs.get('lang', '')}" if "lang" in kwargs else ""),
)
# Fix paths for GitHub Pages
en_html = en_html.replace('href="static/', f'href="{BASE_URL}/static/')
with open(OUTPUT_DIR / "home" / "index.html", "w", encoding="utf-8") as f:
    f.write(en_html)

# Spanish version
es_content = load_markdown_content("es")
es_html = home_template.render(
    content=es_content,
    lang="es",
    app_name="Wedding Site",
    current_year=datetime.now().year,
    url_for=lambda name, **kwargs: f"{BASE_URL}/{name}"
    + (f"/{kwargs.get('lang', '')}" if "lang" in kwargs else ""),
)
# Fix paths for GitHub Pages
es_html = es_html.replace('href="static/', f'href="{BASE_URL}/static/')
with open(OUTPUT_DIR / "home" / "es.html", "w", encoding="utf-8") as f:
    f.write(es_html)

# Create authentication script
print("Creating authentication script...")
auth_js = f"""
// Simple password protection for static site
document.addEventListener('DOMContentLoaded', function() {{
    const loginForm = document.querySelector('form');
    if (loginForm) {{
        loginForm.addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (username === '{USERNAME}' && password === '{PASSWORD}') {{
                // Set session storage to remember logged in status
                sessionStorage.setItem('authenticated', 'true');
                // Hard-code the repository-specific base URL
                window.location.href = '/wedding-site/home/';
            }} else {{
                document.querySelector('.error-message').textContent = 'Invalid username or password';
                document.querySelector('.error-message').style.display = 'block';
            }}
        }});
    }}
    
    // Check if user is authenticated for protected pages
    const isHomePage = window.location.pathname.includes('/home');
    if (isHomePage && sessionStorage.getItem('authenticated') !== 'true') {{
        // Hard-code the repository-specific base URL
        window.location.href = '/wedding-site/';
    }}
    
    // Add logout functionality
    const logoutLink = document.createElement('a');
    logoutLink.href = '#';
    logoutLink.textContent = 'Logout';
    logoutLink.style.cssText = 'position: absolute; top: 10px; right: 20px; color: #5c8d89;';
    logoutLink.addEventListener('click', function(e) {{
        e.preventDefault();
        sessionStorage.removeItem('authenticated');
        // Hard-code the repository-specific base URL
        window.location.href = '/wedding-site/';
    }});
    
    if (isHomePage) {{
        document.body.appendChild(logoutLink);
    }}
}});
"""

with open(OUTPUT_DIR / "static" / "auth.js", "w", encoding="utf-8") as f:
    f.write(auth_js)

# Update templates to include auth.js
with open(OUTPUT_DIR / "index.html", "r", encoding="utf-8") as f:
    login_html = f.read()

login_html = login_html.replace(
    "</body>", f'<script src="{BASE_URL}/static/auth.js"></script>\n</body>'
)

with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(login_html)

for html_file in [OUTPUT_DIR / "home" / "index.html", OUTPUT_DIR / "home" / "es.html"]:
    with open(html_file, "r", encoding="utf-8") as f:
        page_html = f.read()

    page_html = page_html.replace(
        "</body>", f'<script src="{BASE_URL}/static/auth.js"></script>\n</body>'
    )

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(page_html)

# Create deployment instructions
print("Creating deployment instructions...")
with open(OUTPUT_DIR / "README.md", "w", encoding="utf-8") as f:
    f.write(
        """# Wedding Website - Static Version

This is the static version of the wedding website, ready for deployment to GitHub Pages.

## Deployment Steps

1. Push these files to the `gh-pages` branch of your repository:

```bash
# Assuming you're in the root of your project
cd site
git init
git add .
git commit -m "Deploy wedding site to GitHub Pages"
git branch -M gh-pages
git remote add origin https://github.com/yourusername/wedding-site.git
git push -u origin gh-pages -f
```

2. In your GitHub repository settings, configure GitHub Pages to use the `gh-pages` branch.

3. Your site will be available at https://yourusername.github.io/wedding-site/

## Login Credentials

- Username: `{USERNAME}`
- Password: `{PASSWORD}`

Note: This is a client-side authentication for simplicity. For a more secure solution, consider using a proper backend authentication system.
""".format(USERNAME=USERNAME, PASSWORD=PASSWORD)
    )

print(f"Static site generated in {OUTPUT_DIR}!")
print("Next steps:")
print("1. Run: cd site")
print("2. Initialize a git repository")
print("3. Push to the gh-pages branch of your GitHub repository")
print("4. Configure GitHub Pages to use the gh-pages branch")
