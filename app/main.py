from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.auth import authenticate_user, create_access_token, get_current_user
from app.markdown_helper import load_markdown_content


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=3600, #1 hour
)

app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


# Routes
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to login page"""
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "current_year": datetime.now().year,
        },
    )


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handle login form submission"""
    authenticated = authenticate_user(username, password)

    if not authenticated:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password",
                "current_year": datetime.now().year,
            },
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    # Store token in session
    request.session["access_token"] = access_token

    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/home", response_class=HTMLResponse)
@app.get("/home/{lang}", response_class=HTMLResponse)
async def home(request: Request, lang: Optional[str] = "en"):
    """Home page with wedding content"""
    # Check for access token in session
    access_token = request.session.get("access_token")
    if not access_token:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    try:
        # Validate token (without using dependency for simplicity)
        username = get_current_user(token=access_token)
    except HTTPException:
        # If token is invalid, redirect to login
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Get content based on language
    content = load_markdown_content(lang)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "content": content,
            "lang": lang,
            "app_name": settings.APP_NAME,
            "current_year": datetime.now().year,
        },
    )


@app.get("/logout")
async def logout(request: Request):
    """Logout and clear session"""
    request.session.clear()
    return RedirectResponse(url="/login")
