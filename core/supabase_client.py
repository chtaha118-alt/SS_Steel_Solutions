import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Find .env in the same directory as this Python file
env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL not found in .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY not found in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Supabase connected successfully!")