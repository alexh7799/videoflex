# Videoflix – Django Video Streaming Platform

This project is a video streaming platform based on Django and Django REST Framework. It supports video uploads, automatic HLS conversion, thumbnails, authentication, and serving videos and images via API endpoints.

## Features

- User authentication (JWT, Cookie)
- Video upload and management
- Automatic HLS conversion (ffmpeg)
- Thumbnails for videos
- API endpoints for video list, manifest, and segments
- Serving media files via `/media/`
- Static files via Whitenoise
- Docker and PostgreSQL support

## Requirements

- Python 3.12+
- Docker & Docker Compose (recommended)
- ffmpeg (for local development)
- PostgreSQL (default, SQLite possible for development)

## Installation & Startup

### 1. Clone the repository

```bash
git clone git@github.com:alexh7799/videoflex.git
cd videoflix
```

### 2. Configure environment variables

Copy `.env.template` to `.env` and adjust the values (e.g. database, superuser, email).

```bash
cp .env.template .env
```

### 3. Using Docker (recommended)

```bash
docker-compose up --build
```

- The database and backend will start automatically.

### 4. Local development (without Docker)

1. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Migrate the database:

    ```bash
    python manage.py migrate
    ```

4. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

5. Install ffmpeg (if not already installed).
6. Start the server:

    ```bash
    python manage.py runserver
    ```

### 5. Media and static files

- Media files are stored in `media/` and served by Django in debug mode.
- For production, use a web server like nginx for `/media/`.
- Static files are served via Whitenoise.

## Usage

- Backend available at `http://localhost:8000/`

## Notes for other systems

- Adjust paths in `settings.py` (`MEDIA_ROOT`, `STATIC_ROOT`) if needed.
- ffmpeg must be installed and available in the system PATH.
- Docker volumes and ports can be changed in `docker-compose.yml`.
- For production: Set up a web server (nginx) for `/media/`.

**Enjoy using Videoflix!**
