# Strava Routes on Map

This app lets you sync your Strava activities, store them in a database, and visualize your routes on an interactive map in your browser.

## Features

- **Strava Sync:** Import your activities (Walk, Run, Ride) from Strava, including GPS route data.
- **Filtering:** Filter activities by date range and activity type.
- **Map Visualization:** See all your routes on a map.
- **Efficient Data Handling:** Coordinates are deduplicated and precision-reduced for performance.
- **API Documentation:** Interactive Swagger UI docs for all endpoints.
- **Docker Support:** Easy scripts for running a development MongoDB instance.

## Technologies used

- Python with FastAPI
- Pydantic
- MongoDB
- Strava API
- Docker with Docker-compose
- Simple HTML, CSS and vanilla JS for UI
- Leaflet map with Leaflet.heat

## Typical Workflow

1. Enter your API key and Strava token in the web app.
2. Sync your activities from Strava, optionally filtering by date.
3. The backend fetches and stores your activities and route data.
4. View your activity heatmap on the map, with further filtering options.

## Setup and run locally

1. Install Python 3.12.x and set up the virtual environment.

   ```bash
   pyenv install 3.12.10
   pyenv local 3.12.10
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables into the `.env` file.

   ```bash
   # Mongo DB connection string and database name
   MONGODB_URI=
   MONGODB_NAME=

   # Root path on the server where the script is running
   ROOT_PATH=

   # Secret string to be used for hashing
   API_SECRET=

   ```

## API

Dev database:

```bash
# Start the db in Docker:
./dev-db.sh start

# Stop the db:
./dev-db.sh stop

# Clear the db container and volumes:
./dev-db.sh clear
```

Run in local:

```bash
fastapi dev api/main.py
```

Open your browser:

- Web app: `http://localhost:8000/`
- Api docs: `http://localhost:8000/docs`

Publish new docker image:

```bash
cd api

./deploy.sh
```
