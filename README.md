# StarChaser 🌌

**The Premier Star Gazing Site Visibility App**

StarChaser helps you find the best nearby locations for experiencing dark, clear skies. 

## Tech Stack

StarChaser is a full-stack application with a React Native Expo frontend and a FastAPI backend, powered by PostgreSQL + PostGIS.

Frontend  
- React Native  
- Expo  

Backend  
- FastAPI  
- Uvicorn  

Database  
- PostgreSQL  
- PostGIS  

## Prerequisites

- Node.js + npm  
- Python 3.10+  
- PostgreSQL with PostGIS enabled  
- uvicorn  
- Expo Go (mobile app or emulator)  

## Database Setup

Install PostgreSQL (Windows):  
https://www.postgresql.org/download/windows/

Create the database:
```sql
CREATE DATABASE "StarChaser";
```

Migrations and seeding data:
```bash
cd backend
alembic upgrade head
python -m scripts.seed_sites
```

Install backend dependencies:
```bash
pip install -r requirements.txt
```

Get localsettings.json from another developer and place it in the backend/ directory.

Run Backend:
```bash
cd backend/
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

On startup, the backend runs a visibility precompute job by default. To skip it (faster startup):
```bash
cd backend/
set SKIP_VISIBILITY_JOB=1
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```
(On Unix/macOS use `export SKIP_VISIBILITY_JOB=1` instead of `set`.)

Test your backend is setup by navigating to http://192.168.1.18:3000/docs (or whatever the URL is from ipconfig) and hit an endpoint!

## Tests
StarChaser has a test suite powered with pytest

To run all tests:
```bash
cd backend/
python -m pytest
```

## Frontend Setup

Create .env file

run ipconfig

Find the line IPv4 Address. . . . . . . . . . . : 192.168.1.18

Set the backend URL in .env:

EXPO_PUBLIC_BACKEND_API_URL=http://192.168.1.18:3000

Run frontend:
```bash
cd frontend/
npx expo start --clear
```

## "Prod" Notes
GoDaddy -> thestarchaser.com

Cloudflare -> URL redirection

```bash
npm run dev
```

Runs API + Expo + Cloudflare tunnel. On startup, the API runs a visibility precompute job by default. To skip it for faster startup:
```bash
npm run dev:skip-job
```

Get package.json from dev to run. Requires setting up cloudflare.

Requirements:
```bash
npm i concurrently cross-env
```

To access website:
Download expo go.
enter in url: exp://ya5evyg-anonymous-8081.exp.direct
Enjoy!
(requires server running - ping Kyle if you want to test!)

## Notes

Can either run frontend on Expo Go from your phone or download an emulator like BlueStacks and use Expo Go there.

FastAPI Best Practice Resources:

https://fastapi.tiangolo.com/learn/ (main site)

https://github.com/zhanymkanov/fastapi-best-practices (good community repo)


## Troubleshooting

If getting an errror w/ network
re-run ipconfig and update .env file

Your phone needs to be connected to your wifi (running on the same network)

To debug add a launch.json in the .vscode folder. Then simply set break points and debug! To skip the visibility job on startup (faster), add `"env": { "SKIP_VISIBILITY_JOB": "1" }` to the configuration.
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI (uvicorn)",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "cwd": "${workspaceFolder}/backend",
      "args": [
        "main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "3000",
        "--reload"
      ],
      "console": "integratedTerminal"
    }
  ]
}
```


## Contact Info
thestarchaserofficial@gmail.com