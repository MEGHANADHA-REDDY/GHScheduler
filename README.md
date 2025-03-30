# Healthcare Schedule Generator

A Flask-based web application for managing healthcare worker schedules with support for multiple shift types.

## Features

- Multiple shift types (A, B, C, G1, G2)
- Weekly schedule view
- Hourly schedule view
- Caregiver management
- Interactive calendar interface
- Real-time updates
- PostgreSQL database support

## Shift Types

- A Shift: 6:00 AM - 2:00 PM
- B Shift: 4:00 PM - 12:00 AM
- C Shift: 12:00 AM - 8:00 AM
- G1 Shift: 12:00 PM - 8:00 PM
- G2 Shift: 9:00 AM - 5:00 PM

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MEGHANADHA-REDDY/GHScheduler.git
cd GHScheduler
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database URL (required in production)
- `RENDER`: Set to 'true' in production
- `SECRET_KEY`: Flask secret key
- `FLASK_DEBUG`: Set to '1' for debug mode
- `PORT`: Application port (default: 5000)

## Deployment

The application is configured for deployment on Render with PostgreSQL database support.

1. Create a new PostgreSQL database in Render
2. Set up the web service with the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
3. Configure environment variables in Render dashboard

## License

MIT License 