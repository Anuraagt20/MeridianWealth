from pathlib import Path
import os

from dotenv import load_dotenv


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

FRONTEND_DIR = PROJECT_ROOT / "frontend"

TEMPLATES_DIR = FRONTEND_DIR / "templates"

STATIC_DIR = FRONTEND_DIR / "static"


# ==========================================================
# Database
# ==========================================================

DB_PATH = DATA_DIR / "meridian_wealth.db"


# ==========================================================
# Environment Variables
# ==========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ==========================================================
# Validation
# ==========================================================

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. "
        "Please add it to your .env file."
    )