# Videoflix – Django Video Streaming Plattform

Dieses Projekt ist eine Video-Streaming-Plattform auf Basis von Django und Django REST Framework. Es unterstützt Video-Uploads, automatische HLS-Konvertierung, Thumbnails, Authentifizierung und das Ausliefern von Videos und Bildern über API-Endpunkte.

## Features

- Benutzer-Authentifizierung (JWT, Cookie)
- Video-Upload und Verwaltung
- Automatische HLS-Konvertierung (ffmpeg)
- Thumbnails für Videos
- API-Endpunkte für Videolisten, Manifest und Segmente
- Auslieferung von Medien-Dateien über `/media/`
- Statische Dateien über Whitenoise
- Docker- und PostgreSQL-Support

## Voraussetzungen

- Python 3.12+
- Docker & Docker Compose (empfohlen)
- ffmpeg (für lokale Entwicklung)
- PostgreSQL (Standard, SQLite für Entwicklung möglich)

## Installation & Start

### 1. Repository klonen

```bash
git clone git@github.com:alexh7799/videoflex.git
cd videoflix
```

### 2. Umgebungsvariablen anpassen

Kopiere die `.env.template` zu `.env` und passe die Werte an (z.B. Datenbank, Superuser, E-Mail).

```bash
cp .env.template .env
```

### 3. Docker verwenden (empfohlen)

```bash
docker-compose up --build
```

- Die Datenbank und das Backend werden automatisch gestartet.

### 4. Lokale Entwicklung (ohne Docker)

1. Virtuelle Umgebung erstellen und aktivieren:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

2. Abhängigkeiten installieren:

    ```bash
    pip install -r requirements.txt
    ```

3. Datenbank migrieren:

    ```bash
    python manage.py migrate
    ```

4. Superuser erstellen:

    ```bash
    python manage.py createsuperuser
    ```

5. ffmpeg installieren (falls nicht vorhanden).
6. Server starten:

    ```bash
    python manage.py runserver
    ```

### 5. Medien- und statische Dateien

- Medien-Dateien liegen unter `media/` und werden im Debug-Modus von Django ausgeliefert.
- Im Produktivbetrieb empfiehlt sich ein Webserver wie nginx für `/media/`.
- Statische Dateien werden über Whitenoise ausgeliefert.

## Nutzung

- Backend erreichbar unter `http://localhost:8000/`

## Hinweise für andere Systeme

- Passe die Pfade in `settings.py` (`MEDIA_ROOT`, `STATIC_ROOT`) ggf. an.
- ffmpeg muss auf dem Zielsystem installiert und im PATH verfügbar sein.
- Docker-Volumes und Ports können in `docker-compose.yml` angepasst werden.
- Für Produktion: Richte einen Webserver (nginx) für `/media/` ein.

**Viel Spaß mit Videoflix!**
