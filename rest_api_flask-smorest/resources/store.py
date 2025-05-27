import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import stores
from schema import StoreSchema, StoreUpdateSchema
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# We now cannot use items {} and stores {}, since now we have connected db, and we have extract data from the tables

# MethodView creates a class, and methods of that class help to route specific endpoints

# Smorest Blueprints help divide API into multiple segments, here we have two parts, shop and items, so two parts, can be many

# Both together build different groups, and internally create class for the group with mehtods defining specific endpoints. 

blp = Blueprint("stores", __name__, description = "Operations on stores")

# So, here, we are trying to build a class store, which would have get and delete methods, which have same enpoint except the http type changes,
# and hence these are combined into one class using methodview, and since we are dealing with /store/<stirng:store_id>, all the routes we have
# defined with same endpoint irrespective of http methods come under this class, and it is defined using blp

# We can understand the beloe class as follows, when blp gets a get req to /store/<string:store_id>, it executes get() function, and 
# when blp receives del req, it executes del(), as simple as that

@blp.route("/store/<int:store_id>")
class StoreRoutesWithId(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     # return {"message", "Store not found"}, 404
        #     # Above line could be modified using abort
        #     abort(404, message = "Store not found")
        
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
    
        # Validating if all the details in the body are available, like we expect store_name, store_type, store_mode
        # if(   "store_name" not in store_data
        # or "store_type" not in store_data
        # or "store_mode" not in store_data
        # ):
        #         abort(404, message = "Details are missing, make sure store_name, store_type, store_mode details are provided.")
        
        # Validating if the given store_id exists, only then record could be updated
        # try:
        #     store = stores[store_id]
        #     store.update(store_data)
        #     return store
        # except KeyError:
        #     abort(404, "Store not found.")
        
        store = StoreModel.query.get(store_id)
        
        if store:
            store.store_name = store_data["store_name"]
            store.store_type = store_data["store_type"]
            store.store_mode = store_data["store_mode"]
        else:
            store = StoreModel(store_id = store_id, **store_data)
        
        db.session.add(store)
        db.session.commit()
        
        return store    
        
    
    def delete(self, store_id):
        # try:
        #     del stores[store_id]
        #     return {"message": f"Store with id {store_id} is deleted."}
        # except KeyError:
        #     abort(404, message = "Store not found.")
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store Record Deleted!"}
            

@blp.route("/store")
class StoreRoutes(MethodView):
    
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
    
        # Validating if all the details in the body are available, like we expect store_name, store_type, store_mode
        # if(   "store_name" not in store_data
        # or "store_type" not in store_data
        # or "store_mode" not in store_data
        # ):
        #         abort(404, message = "Details are missing, make sure store_name, store_type, store_mode details are provided.")
        
        # Validating if the store already exist
        
        # Since we would be making data persistant, using StoreModel and db, we wont be requiring below code
        """
        for store in stores.values():
            if store["store_name"] == store_data["store_name"]:
                abort(400, message = f"Store already exists!")
        
        store_id = uuid.uuid4().hex
        store = {**store_data, "store_id":store_id}
        stores[store_id] = store
        """
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "A store with the name already exists")
        except SQLAlchemyError:
            abort(500, message = "An error occured creating the store.")
        
        return store, 201
        