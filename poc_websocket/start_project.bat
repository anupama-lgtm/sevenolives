@echo off
echo ========================================
echo Django WebSocket POC - Startup Script
echo ========================================
echo.

echo Step 1: Checking if virtual environment exists...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
echo.

echo Step 4: Running migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo Step 5: Starting Django server...
echo.
echo ========================================
echo Server is starting...
echo.
echo Open your browser:
echo   Window 1: http://localhost:8000/window1/
echo   Window 2: http://localhost:8000/window2/
echo.
echo Make sure Redis is running!
echo   (In another terminal, run: redis-server)
echo ========================================
echo.

python manage.py runserver

