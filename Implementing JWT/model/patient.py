from db import db

class PatientModel(db.Model):
    
    __tablename__ = "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    health_issue = db.Column(db.String(150), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), unique=False, nullable=False)
    
    doctor = db.relationship("DoctorModel", back_populates="patients")
    
    