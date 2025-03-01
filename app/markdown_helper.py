import markdown2
import os
from pathlib import Path
from app.config import settings


def load_markdown_content(language: str = "en") -> str:
    """
    Load markdown content based on the specified language
    """
    base_dir = settings.BASE_DIR

    if language == "es":
        markdown_file = base_dir / "markdown_content_es.md"
    else:
        markdown_file = base_dir / "markdown_content_en.md"

    if not markdown_file.exists():
        return "Content not found for the selected language."

    with open(markdown_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_content, extras=["tables", "fenced-code-blocks", "break-on-newline"]
    )

    # Handle image placeholders (English and Spanish)
    html_content = html_content.replace("[Image:", '<div class="image-placeholder">[Image:')
    html_content = html_content.replace("[Imagen:", '<div class="image-placeholder">[Imagen:')
    html_content = html_content.replace("]", ']</div>')
    
    # For actual images when they're available
    html_content = html_content.replace("![[", '<img src="/static/images/')
    html_content = html_content.replace("]]", '">')

    return html_content
