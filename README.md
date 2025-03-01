# Wedding Website

A simple wedding website built with FastAPI that displays wedding information in both English and Spanish, with password protection.

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

## Deploying to Hugging Face Spaces

1. Create a Hugging Face account if you don't have one: https://huggingface.co/join

2. Create a new Space:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name for your space (e.g., "wedding-site")
   - Select "FastAPI" as the SDK
   - Choose "Public" or "Private" visibility (Private is recommended for wedding sites)

3. Clone your repository to Hugging Face:
   ```bash
   git clone https://github.com/YOUR_USERNAME/wedding-site.git
   cd wedding-site
   git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/wedding-site
   git push space main
   ```

4. Set up environment variables in Hugging Face Space:
   - Go to your Space settings
   - Add the following environment variables:
     - `SECRET_KEY`: A secure random string
     - `ALGORITHM`: HS256
     - `ACCESS_TOKEN_EXPIRE_MINUTES`: 10080
     - `USERNAME`: Your chosen username
     - `PASSWORD`: Your secure password
     - `APP_NAME`: "Wedding Site"

5. Your site will automatically build and be available at:
   https://huggingface.co/spaces/YOUR_HF_USERNAME/wedding-site

## License

This project is private and intended for personal use only.

## Acknowledgements

- FastAPI - https://fastapi.tiangolo.com/
- Jinja2 - https://jinja.palletsprojects.com/
- Markdown2 - https://github.com/trentm/python-markdown2
