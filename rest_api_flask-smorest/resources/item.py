import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
# from db import items, stores
from schema import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

# We now cannot use items and stores {}, since now we have connected db, and we have extract data from the tables

# Similar to what we have done for stores

blp = Blueprint("items", __name__, description = "Operations of Items")

@blp.route("/item/<string:item_id>")
class ItemsRoutesUsingId(MethodView):
    
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        
        # We could directly use query(), which is a functionality of SQLAlchemy that would fetch us data
        # try: 
        #     return items[item_id]
        # except KeyError:
        #     #return {"message": "Item not found"}, 404
        #     abort(404, message = "Item not found")
        
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    
    # Updating the item object is not as straightforward as posting or getting, whether one req is hit or multiple, we must make sure 
    # the data for a particular item is updated properly
    # Also, coming to update, if the item exist, we update the item, or if it doesnot exist, then we create new item, but we wont raise
    # error that item with id wont exist, please create one using /post, instead create one here, making things easy for end user.
    
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
    
        # Validating if item_name, quantity, price are given, if not, item cannot be updated
        # if(
        #     "item_name" not in item_data
        #     or "price" not in item_data
        #     or "quantity" not in item_data
        # ):
        #     abort(400, message = "Item cannot be updated, check if all the details of name, price and quantity are provided.")
        
        # try:
        #     item = items[item_id]
        #     item.update(item_data)
        #     return item
        # except KeyError:
        #     abort(400, message = "Item not found.")
        item = ItemModel.query.get(item_id)
        
        if item:
            item.item_name = item_data["item_name"]
            item.price = item_data["price"]
            item.quantity = item_data["quantity"]
        else:
            item = ItemModel(item_id = item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()
        
        return item
    
    def delete(self, item_id):
        # try:
        #     del items[item_id]
        #     return {"message": f"Item with id {item_id} is deleted."}
        # except KeyError:
        #     abort(404, message = "Item not found.")
        
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        
        return {"message": "Item record deleted!"}
            

@blp.route("/item")
class ItemRoutes(MethodView):
    
    # The response here would be a list of items, so in arguments, we would send ItemSchema, but with constraint many=True, telling 
    # marshmallow that this might return many, and here we are sending a list, marshmallow would convert list into json internally
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    # Inorder for post to validate data using Marshmallow, we must tell marshmallow to validate the input data sent to it, which is done using
    # @blp.aruguments(ItemSchema) and this would validate the data, and return an argument to post, and that could be used directly
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
    
        """
        Validation of data, as of now we would try to validate manually, but furtherly we would use marshmallow
        So for now, I am validating if data we get from the req body is valid, like the required fields are here, name, price and quantity are
        also provided, and furtherly, we would also verify if the data provided to these variables are correct, like for price we excpet float, 
        string as name, something in that way. 
        
        As of now, validating if all the required input fields data is provided, for this case store_id, quantity, price and name, and this is
        how basic validation could be done without using Marshmallow.
        """    
        
        # if (
        #     "price" not in item_data
        #     or "store_id" not in item_data
        #     or "item_name" not in item_data
        #     or "quantity" not in item_data
        # ):
        #     abort(404, message = "Please provide all the details of store_id, price, quantity, and item_name fields.")
        
        # Above validation is now taken care by Marshmallow
            
        # Now valdiating if their exist an item which has with same name and same store_id already, that means item already exist.
        # Marshmallow only validates the incoming data, it cannot check the below task, so let it be the way it is.
        
        """
        
        # Since we are using database now, we need not undergo the below validation, we could directly use ItemModel which has the datafields
        # and using that we can populate data into table, basically create row
        
        for item in items.values():
            if (item_data["item_name"] == item["item_name"] 
            and item_data["store_id"] == item["store_id"]):
                abort(404, message = "Item already exists.")
                
        # Validating if the store_id provided does not exists, that mean invalid store, or the store does not exist.
                
        if item_data["store_id"] not in stores:
            # return {"message", "Store not found, Item cannot be added!"}, 404
            abort(404, message = "Store not found, Item cannot be added!")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "item_id":item_id}
        items[item_id] = item
        """
        
        item = ItemModel(**item_data)
        
        # Adding item into db
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured while inserting the item.")
        
        return item, 201
    
    