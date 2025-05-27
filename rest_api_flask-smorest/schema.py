# In this file, we define the schema of the entities, or objects we are working on, for this project, store, and item
# This could be achived by using Marshmallow's Schema and fields Class, and functions.
# Schema is like a blueprint that says what our data should look like, and fields is the 
# Tool used inside the Schema to define each field’s type and rules

from marshmallow import Schema, fields


# We define PlainSchemas first, becasue in models we have defined extra thing that StoreModel qould require list of items, 
# and ItemModle would require one such Store to which the item record is associated with, so initially we'll create PlainSchema, and this
# would be inherited

class PlainItemSchema(Schema):
    item_id = fields.Int(dump_only=True) # We would never expect id from request, we generate as response, and hence dump it in the response, 
                                        # dumping is searializing response to client. 
    item_name = fields.Str(required=True) # When we want some field to be mandatorily sent in request json payload, then we do in this way.
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)

class PlainStoreSchema(Schema):
    store_id = fields.Int(dump_only=True)
    store_name = fields.Str(required=True)
    store_type = fields.Str(required=True)
    store_mode = fields.Str(required=True)
    
class PlainTagSchema(Schema):
    tag_id = fields.Int(dump_only=True)
    tag_name = fields.Str(required=True)

# We inherit Schema, which has some properties, which we would use directly.
# This is for validating info of item, while creating and adding new item
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    
    
# For updating existing item
class ItemUpdateSchema(Schema):
    item_name = fields.Str()
    price = fields.Float()
    quantity = fields.Int()
    store_id = fields.Int()
    
# For store
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))

# For Updating an existing store
class StoreUpdateSchema(Schema):
    store_name = fields.Str()
    store_type = fields.Str()
    store_mode = fields.Str()
    
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema) 
    
    
    
