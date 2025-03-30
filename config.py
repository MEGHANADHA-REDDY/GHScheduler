class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///schedule.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    PORT = 7761

class ShiftConfig:
    SHIFTS = {
        'A': {'name': 'A Shift', 'time': '6:00 AM - 2:00 PM', 'start_hour': 6, 'duration': 8, 'color': '#90EE90'},
        'B': {'name': 'B Shift', 'time': '4:00 PM - 12:00 AM', 'start_hour': 16, 'duration': 8, 'color': '#87CEEB'},
        'C': {'name': 'C Shift', 'time': '12:00 AM - 8:00 AM', 'start_hour': 0, 'duration': 8, 'color': '#DDA0DD'},
        'G': {'name': 'G Shift', 'time': '12:00 PM - 8:00 PM', 'start_hour': 12, 'duration': 8, 'color': '#F0E68C'}
    }
    
    CAREGIVERS = ['CG1', 'CG2', 'CG3', 'CG4', 'CG5', 'CG6', 'CG7', 'CG8']
    SHIFTS_PER_WEEK = 5  # Each caregiver works 5 days
    HOURS_PER_SHIFT = 8  # Each shift is 8 hours
    HOURS_PER_WEEK = 40  # Total weekly hours per caregiver 