# **Welcome to StarChaser!!!**

Frontend:
React Native Expo

Backend:
Fast API

DB:
PostgreSQL and PostgreGIS
https://www.postgresql.org/download/windows/

PreReques:
uvicorn

Create .env file
run ipconfig
Find the line IPv4 Address. . . . . . . . . . . : 192.168.1.18
set variable EXPO_PUBLIC_BACKEND_API_URL=http://192.168.1.18:3000 

Start app: 
cd frontend/
npx expo start --clear

Run Backend:
cd backend/
uvicorn main:app --host 0.0.0.0 --port 3000 --reload

Can either run frontend on Expo Go from your phone or download an emulator like BlueStacks and use Expo Go there.

For now need to be on the same Network as me :)

If getting an errror w/ network
re-run ipconfig and update .env file


