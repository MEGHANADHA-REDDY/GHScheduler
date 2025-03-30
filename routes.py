from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY
from models import Caregiver, Shift, db
from config import ShiftConfig

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/calendar')
def calendar_view():
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())  # Start from Monday
    dates = list(rrule(DAILY, count=7, dtstart=start_date))
    
    shifts = Shift.query.filter(
        Shift.date >= start_date,
        Shift.date < start_date + timedelta(days=7)
    ).order_by(Shift.date, Shift.shift_type).all()
    
    return render_template('calendar.html', dates=dates, shifts=shifts)

@views.route('/hourly')
def hourly_view():
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())  # Start from Monday
    dates = list(rrule(DAILY, count=7, dtstart=start_date))
    
    shifts = Shift.query.filter(
        Shift.date >= start_date,
        Shift.date < start_date + timedelta(days=7)
    ).order_by(Shift.date, Shift.shift_type).all()
    
    return render_template('hourly.html', dates=dates, shifts=shifts)

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
                         shifts=shifts,
                         shift_types=ShiftConfig.SHIFTS)

@views.route('/add_shift', methods=['POST'])
def add_shift():
    try:
        caregiver_id = request.form.get('caregiver_id')
        shift_type = request.form.get('shift_type')
        date_str = request.form.get('date')
        
        if not all([caregiver_id, shift_type, date_str]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Convert date string to date object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if shift already exists
        existing_shift = Shift.query.filter_by(
            date=date,
            shift_type=shift_type
        ).first()
        
        if existing_shift:
            return jsonify({'error': 'Shift already assigned'}), 400
            
        # Check if shift type is valid
        if shift_type not in ShiftConfig.SHIFTS:
            return jsonify({'error': 'Invalid shift type'}), 400
            
        # Create new shift
        new_shift = Shift(
            date=date,
            shift_type=shift_type,
            caregiver_id=caregiver_id
        )
        
        db.session.add(new_shift)
        db.session.commit()
        
        return jsonify({'message': 'Shift added successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@views.route('/remove_shift', methods=['POST'])
def remove_shift():
    try:
        shift_id = request.form.get('shift_id')
        if not shift_id:
            return jsonify({'error': 'Missing shift ID'}), 400
            
        shift = Shift.query.get(shift_id)
        if not shift:
            return jsonify({'error': 'Shift not found'}), 404
            
        db.session.delete(shift)
        db.session.commit()
        
        return jsonify({'message': 'Shift removed successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 