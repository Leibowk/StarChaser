# StarChaser 🌌

StarChaser is a full-stack application built with a React Native Expo frontend and a FastAPI backend, backed by PostgreSQL + PostGIS.

## Tech Stack

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
python -m scripts.seed.seed_sites
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


## Notes

Can either run frontend on Expo Go from your phone or download an emulator like BlueStacks and use Expo Go there.


## Troubleshooting

If getting an errror w/ network
re-run ipconfig and update .env file

For now need to be on the same Network as me :)