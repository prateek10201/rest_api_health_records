from db import db

# We are basically defining the entity, like we do for spring data jpa, like @Entity, here we have (db.Model), it maps attributes to columns
# in sql, and table rows as python object

class ItemModel(db.Model):
    # Defining the name of the table
    
    __tablename__ = "items"
    
    # Defining columns
    # Below, we are defining primary key, defuault auto_increment is enabled, postgres would take care of it
    
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"), unique=False, nullable=False)
    
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
    