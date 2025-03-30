import os

class Config:
    # Get the directory where the application is running
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL', '')
    
    # Handle both 'postgres://' and 'postgresql://' URL formats
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Use PostgreSQL in production (Render) and SQLite in development
    if os.environ.get('RENDER', ''):
        # We're on Render, use PostgreSQL
        if not database_url:
            raise ValueError('DATABASE_URL environment variable is required when running on Render')
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Local development, use SQLite
        SQLALCHEMY_DATABASE_URI = database_url or \
            'sqlite:///' + os.path.join(base_dir, 'schedule.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    DEBUG = True  # Enable debug mode by default
    PORT = int(os.environ.get('PORT', 5000))

class ShiftConfig:
    SHIFTS = {
        'A': {'name': 'A Shift', 'time': '6:00 AM - 2:00 PM', 'start_hour': 6, 'duration': 8, 'color': '#90EE90'},
        'B': {'name': 'B Shift', 'time': '4:00 PM - 12:00 AM', 'start_hour': 16, 'duration': 8, 'color': '#87CEEB'},
        'C': {'name': 'C Shift', 'time': '12:00 AM - 8:00 AM', 'start_hour': 0, 'duration': 8, 'color': '#DDA0DD'},
        'G1': {'name': 'G1 Shift', 'time': '12:00 PM - 8:00 PM', 'start_hour': 12, 'duration': 8, 'color': '#F0E68C'},
        'G2': {'name': 'G2 Shift', 'time': '9:00 AM - 5:00 PM', 'start_hour': 9, 'duration': 8, 'color': '#FFB6C1'}
    }
    
    CAREGIVERS = ['CG1', 'CG2', 'CG3', 'CG4', 'CG5', 'CG6', 'CG7', 'CG8']
    SHIFTS_PER_WEEK = 5  # Each caregiver works 5 days
    HOURS_PER_SHIFT = 8  # Each shift is 8 hours
    HOURS_PER_WEEK = 40  # Total weekly hours per caregiver 
