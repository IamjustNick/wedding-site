# Wedding Website

A simple wedding website built with FastAPI and protected with password authentication.

This is a dead simple project I am using to test Claude's new coding  assistant features.

## Features

- Password-protected content
- Bilingual support (English and Spanish)
- Markdown content rendering

## Development Setup

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)

### Installation

1. Clone the repository

2. Set up the Python environment (I am using pyenv):
```bash
# Create a virtual environment
pyenv virtualenv 3.11.6 wedding-site
pyenv local wedding-site

# Install dependencies
pip install poetry
poetry install
```


### Running the Development Server

```bash
python run.py
```

The application will be available at http://localhost:8000

## Usage

  - Access with the configured login and password
### Environment Variables

The application uses environment variables for configuration:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file to set your own values:
   ```
   # Security
   SECRET_KEY=your_secure_random_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 1 week

   # Authentication
   USERNAME=your_chosen_username
   PASSWORD=your_secure_password

   # Application settings
   APP_NAME="Wedding Site"
   ```

3. For GitHub Pages deployment, you'll need to add these environment variables as GitHub Secrets:
   - Go to your GitHub repository
   - Navigate to Settings → Secrets → Actions
   - Add each variable as a new secret

## Deploying to GitHub Pages

### Automatic Deployment (Recommended)

1. Create a GitHub repository for your website

2. Add the following secrets in your GitHub repository (Settings → Secrets → Actions):
   - `SECRET_KEY`: A secure random string
   - `ALGORITHM`: HS256
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: 10080 (1 week)
   - `USERNAME`: Your chosen username
   - `PASSWORD`: Your secure password
   - `APP_NAME`: "Wedding Site" (or your custom name)

3. Push your code to the `main` branch

4. GitHub Actions will automatically build and deploy your site to the `gh-pages` branch

5. Configure GitHub Pages to serve from the `gh-pages` branch in your repository settings

### Manual Deployment

If you prefer to deploy manually:

1. Create a GitHub repository for your website

2. Generate the static site locally:
   ```bash
   python deploy_to_github.py
   ```

3. Push the generated files to GitHub:
   ```bash
   cd site
   git init
   git add .
   git commit -m "Deploy wedding site to GitHub Pages"
   git branch -M gh-pages
   git remote add origin https://github.com/YOUR_USERNAME/wedding-site.git
   git push -u origin gh-pages -f
   ```

4. Configure GitHub Pages to serve from the `gh-pages` branch

## License

This project is private and intended for personal use only.

## Acknowledgements

- FastAPI - https://fastapi.tiangolo.com/
- Jinja2 - https://jinja.palletsprojects.com/
- Markdown2 - https://github.com/trentm/python-markdown2
