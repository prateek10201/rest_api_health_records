from db import db

class StoreModel(db.Model):
    
    __tablename__ = "stores"
    
    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(80), unique=True, nullable=False)
    store_type = db.Column(db.String(80), nullable=False)
    store_mode = db.Column(db.String(80), nullable=False)
    
    # dynamic, it dynamically loads the store associated with particular item_id and populates it, and cascade = all, delete
    # when a store with specific id is deleted, delete all associated items, because item must exist only of store exist
    
    
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    