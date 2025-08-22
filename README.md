# Travel Booking Application

A Django-based travel booking system to manage users, travel options, and bookings.

## Features

- User registration, login, and authentication
- Browse and filter travel options by type, date, and destination
- Book and cancel travel options with seat availability checks
- View booking history

==========================
|  Setup Instructions    |
==========================
1). Prerequisites
- Python 3.x
- MySQL Server (or adjust for your preferred database)
- Git

2).Clone the repository:
    git clone https://github.com/PinjariAbdul/travel_bookingsystem.git
   cd travel_bookingsystem


3). Create and activate a virtual environment
   
   python -m venv env

Windows
env\Scripts\activate

Linux/macOS
source env/bin/activate

4). Install dependencies

pip install -r requirements.txt


5).Create `.env` file

Create a `.env` file in the project root (same as manage.py) and add the following:

 - SECRET_KEY=your_secret_key_here
 - DEBUG=True
 - DB_NAME=travelbooking
 - DB_USER=root
 - DB_PASSWORD=your_db_password
 - DB_HOST=localhost
 - DB_PORT=3306


6). Apply migrations

   python manage.py migrate



5). Run the development server

python manage.py runserver

Open your browser and go to `http://127.0.0.1:8000/` to access the app.

---
