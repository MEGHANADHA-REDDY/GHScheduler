from flask_sqlalchemy import SQLAlchemy
from config import ShiftConfig

db = SQLAlchemy()

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shifts = db.relationship('Shift', backref='caregiver', lazy=True)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shift_type = db.Column(db.String(1), nullable=False)  # A, B, C, or G
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)

    @property
    def time_range(self):
        return ShiftConfig.SHIFTS[self.shift_type]['time']
    
    @property
    def start_hour(self):
        return ShiftConfig.SHIFTS[self.shift_type]['start_hour']
    
    @property
    def duration_hours(self):
        return ShiftConfig.SHIFTS[self.shift_type]['duration']

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        # Create caregivers if they don't exist
        if not Caregiver.query.first():
            for name in ShiftConfig.CAREGIVERS:
                db.session.add(Caregiver(name=name))
            db.session.commit() 