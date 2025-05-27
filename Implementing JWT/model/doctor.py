from db import db

class DoctorModel(db.Model):
    
    __tablename__ = "doctors"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    speciality = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    
    # Since one doc can have many patients
    patients = db.relationship("PatientModel", back_populates="doctor", lazy="dynamic", cascade="all, delete")