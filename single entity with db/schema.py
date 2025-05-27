from marshmallow import Schema, fields

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    gender = fields.Str(required=True)
    health_issue = fields.Str(required=True)
    
    
class PatientUpdateSchema(Schema):
    name = fields.Str()
    age = fields.Int()
    gender = fields.Str()
    health_issue = fields.Str()