from flask_sqlalchemy import SQLAlchemy
from config import ShiftConfig, Config
import logging
import time
import os
from sqlalchemy.exc import SQLAlchemyError

# Get the DATABASE_URL from environment variable
database_url = os.getenv('DATABASE_URL')

# If using Render, modify the URL to work with SQLAlchemy
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shifts = db.relationship('Shift', backref='caregiver', lazy=True)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shift_type = db.Column(db.String(3), nullable=False)  # A, B, C, G1, or G2
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
    max_retries = 3
    retry_delay = 2  # seconds
    
    # Configure the SQLAlchemy database URI from Config class
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    
    # Initialize the db with the app
    db.init_app(app)
    
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempting database initialization (attempt {attempt + 1}/{max_retries})")
            
            with app.app_context():
                # Create all tables if they don't exist
                db.create_all()
                
                # Only initialize caregivers in development or if forced
                if not os.environ.get('RENDER', '') or os.environ.get('FORCE_INIT_DB', ''):
                    # Check if we need to initialize caregivers
                    caregiver_count = Caregiver.query.count()
                    if caregiver_count == 0:
                        logging.info("No caregivers found. Initializing caregivers...")
                        for name in ShiftConfig.CAREGIVERS:
                            # Check if caregiver already exists
                            if not Caregiver.query.filter_by(name=name).first():
                                caregiver = Caregiver(name=name)
                                db.session.add(caregiver)
                        
                        db.session.commit()
                        logging.info(f"Successfully initialized {len(ShiftConfig.CAREGIVERS)} caregivers")
                    else:
                        logging.info(f"Found {caregiver_count} existing caregivers")
                else:
                    logging.info("Skipping caregiver initialization in production environment")
                
                return True

        except SQLAlchemyError as e:
            logging.error(f"Database error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("Failed to initialize database after all retries")
                return False
        except Exception as e:
            logging.error(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("Failed to initialize database after all retries")
                return False 
