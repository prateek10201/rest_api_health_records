from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from model import PatientModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schema import PatientSchema, PatientUpdateSchema

blp = Blueprint("patients", __name__ , description = "Operations on Patient Information")

@blp.route("/patients/<int:id>")
class PatientRoutesWithId(MethodView):
    
    @blp.response(200, PatientSchema)
    def get(self, id):
        patient = PatientModel.query.get_or_404(id)
        return patient
    
    @blp.arguments(PatientUpdateSchema)
    @blp.response(201, PatientUpdateSchema)
    def put(self, patient_data, id):
        
        patient = PatientModel.query.get_or_404(id)
        
        if patient.name != patient_data["name"]:
            abort(400, message = "Patient name can't be updated.")
        elif patient.name == patient_data["name"]:
            patient.age = patient_data["age"]
            patient.gender = patient_data["gender"]
            patient.health_issue = patient_data["health_issue"]
        else:
            abort(400, message = f"Patient record with id : {id} does not exist, create one.")
            
        db.session.add(patient)
        db.session.commit()
        
        return patient
    
    def delete(self, id):
        
        patient = PatientModel.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()
        
        return {"message": f"Patient with id - {id} is deleted successfully."}
    
    
@blp.route("/patients")
class PatientListRoutes(MethodView):
    
    @blp.response(200, PatientSchema(many=True))
    def get(self):
        
        patients = PatientModel.query.all()
        return patients
    
    @blp.arguments(PatientSchema)
    @blp.response(201, PatientSchema)
    def post(self, patient_data):
        
        patient = PatientModel(**patient_data)
        
        try:
            db.session.add(patient)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "A patient with name (Fristname + Lastname) already exist!")
        except SQLAlchemyError:
            abort(500, message = "An error occured in creating Patient Record!")
            
        return patient