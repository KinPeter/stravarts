# Strava routes on map

## Setup and run

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
