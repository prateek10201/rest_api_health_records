from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from model import DoctorModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schema import DoctorSchema, DoctorUpdateSchema, PatientSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("doctors", __name__, description = "Operations related to Doctor Entity")
    
@blp.route("/doctors")
class DoctorListRoutes(MethodView):
    
    @jwt_required()
    @blp.response(200, DoctorSchema(many=True))
    def get(self):
        doctors = DoctorModel.query.all()
        
        print(DoctorModel.query.all())
        
        return doctors
    
    @jwt_required()
    @blp.arguments(DoctorSchema)
    @blp.response(201, DoctorSchema)
    def post(self, doctor_data):
        if DoctorModel.query.filter_by(email=doctor_data["email"]).first():
            abort(409, message="Email already registered.")
            
        doctor = DoctorModel(**doctor_data)
        
        try:
            db.session.add(doctor)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured in creating Doctor Record!")
            
        return doctor
    

@blp.route("/doctors/<int:doctor_id>")
class DoctorRoutesUsingId(MethodView):
    
    @jwt_required()
    @blp.response(200, DoctorSchema)
    def get(self, doctor_id):
        doctor = DoctorModel.query.get_or_404(doctor_id)
        
        print(f"Looking up doctor with id: {doctor_id}")
        print(DoctorModel.query.all())
        return doctor
    
    @jwt_required()
    @blp.arguments(DoctorUpdateSchema)
    @blp.response(201, DoctorUpdateSchema)
    def put(self, doctor_data, doctor_id):
        
        doctor = DoctorModel.query.get(doctor_id)
        
        print(f"Looking up doctor with id: {doctor_id}")
        print(DoctorModel.query.all())
        
        if doctor.email != doctor_data["email"]:
            abort(400, message = "Email cannot be modified")
        elif doctor.email == doctor_data["email"]:
            doctor.name = doctor_data["name"]
            doctor.speciality = doctor_data["speciality"]
            doctor.phonenumber = doctor_data["phonenumber"]
            doctor.dob = doctor_data["dob"]
        else:
            abort(401, message = f"Doctor record with id : {doctor_id} does not exist, create one.")
            
        db.session.add(doctor)
        db.session.commit()
        
        return doctor

    @jwt_required()
    def delete(self, doctor_id):
        doctor = DoctorModel.query.get_or_404(doctor_id)
        
        print(f"Looking up doctor with id: {doctor_id}")
        print(DoctorModel.query.all())
        
        db.session.delete(doctor)
        db.session.commit()
        return {"message": f"Doctor record with id : {doctor_id} deleted successfully."}
    
@blp.route("/doctors/<int:doctor_id>/patients")
class DoctorPatientList(MethodView):
    
    @jwt_required()
    @blp.response(200, PatientSchema(many=True))
    def get(self, doctor_id):
        doctor = DoctorModel.query.get_or_404(doctor_id)
        return doctor.patients