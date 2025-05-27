from marshmallow import Schema, fields, validate, ValidationError, validates
import re

class PlainPatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(["male", "female", "other"]))
    health_issue = fields.Str(required=True)
    
class PlainDoctorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    speciality = fields.Str(required=True)
    email = fields.Email(required=True)
    phonenumber = fields.Str(required=True)
    dob = fields.Date(required=True)
    
    @validates("phonenumber")
    def validate_phone_number(self, phonenumber, **kwargs):
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, phonenumber):
            raise ValidationError("Invalid phone number format.")
    
class PatientSchema(PlainPatientSchema):
    doctor_id = fields.Int(required=True, load_only=True)
    doctor = fields.Nested(PlainDoctorSchema(), dump_only=True)
    
class DoctorSchema(PlainDoctorSchema):
    patients = fields.List(fields.Nested(PlainPatientSchema()), dump_only=True)
    
class PatientUpdateSchema(Schema):
    name = fields.Str()
    age = fields.Int()
    gender = fields.Str()
    health_issue = fields.Str()
    # doctor_id = fields.Int()
        
        
class DoctorUpdateSchema(Schema):
    name = fields.Str()
    speciality = fields.Str()
    email = fields.Email()
    phonenumber = fields.Str()
    dob = fields.Date()
    
    @validates("phonenumber")
    def validate_phone_number(self, phonenumber, **kwargs):
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, phonenumber):
            raise ValidationError("Invalid phone number format.")