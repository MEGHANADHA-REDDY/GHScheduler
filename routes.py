from flask import Blueprint, render_template
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY
from models import Caregiver, Shift

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/calendar')
def calendar_view():
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())  # Start from Monday
    end_date = start_date + timedelta(days=7)  # One week
    
    dates = list(rrule(DAILY, count=7, dtstart=start_date))  # Only 7 days
    
    shifts = Shift.query.filter(
        Shift.date >= start_date,
        Shift.date < end_date
    ).order_by(Shift.date, Shift.shift_type).all()
    
    return render_template('calendar.html', dates=dates, shifts=shifts)

@views.route('/hourly')
def hourly_view():
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())  # Start from Monday
    end_date = start_date + timedelta(days=7)  # One week
    
    # Generate time slots for 24 hours
    time_slots = []
    for hour in range(24):
        if hour == 0:
            slot = "12:00 AM - 1:00 AM"
        elif hour < 12:
            slot = f"{hour}:00 AM - {hour+1}:00 AM"
        elif hour == 12:
            slot = "12:00 PM - 1:00 PM"
        else:
            slot = f"{hour-12}:00 PM - {(hour-12+1)}:00 PM"
        time_slots.append(slot)
    
    # Get all shifts for the week
    shifts = Shift.query.filter(
        Shift.date >= start_date,
        Shift.date < end_date
    ).order_by(Shift.date, Shift.shift_type).all()
    
    # Create a week schedule
    week_dates = list(rrule(DAILY, count=7, dtstart=start_date))
    
    return render_template('hourly.html', 
                         time_slots=time_slots,
                         dates=week_dates,
                         shifts=shifts)

@views.route('/caregivers')
def caregiver_view():
    caregivers = Caregiver.query.all()
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())  # Start from Monday
    end_date = start_date + timedelta(days=7)  # One week
    
    # Get shifts for the current week
    shifts = Shift.query.filter(
        Shift.date >= start_date,
        Shift.date < end_date
    ).order_by(Shift.date, Shift.shift_type).all()
    
    # Create a week schedule
    week_dates = list(rrule(DAILY, count=7, dtstart=start_date))
    
    return render_template('caregivers.html', 
                         caregivers=caregivers,
                         week_dates=week_dates,
                         shifts=shifts) 