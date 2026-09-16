Installation Packages
uv init

uv add fastapi uvicorn python-dotenv groq
uv add "psycopg[binary]"
uv add sqlalchemy
uv add "pwdlib[argon2]"
uv add python-jose
uv sync

Running the application
uv run uvicorn src.video_calling_app.main:app --reload
