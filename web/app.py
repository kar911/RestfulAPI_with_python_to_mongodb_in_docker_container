from flask import Flask, jsonify, request #importing  usefull packages
from flask_restful import Api, Resource #importing  usefull packages
from pymongo.errors import DocumentTooLarge,CollectionInvalid,InvalidName,OperationFailure
#importing DocumentTooLarge CollectionInvalid InvalidName OperationFailure from pymongo.error as these are sufficent for this assignment
from pymongo import MongoClient
#importing MongoClient from pymongo

#instantiate Flask
app = Flask(__name__)
#dynamic object
api = Api(app)

#creating a mongo client instance
client=MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                        authSource="admin")
#providing database name to mybd
mydb = client["newdb"]
#providing collection name to user
user = mydb["colln"]

#checking api is running or not
#made a  class Message that inherit Resource and get is a method from Resource
class Message(Resource):
  def get(self):
    return jsonify({"message":"API relay working"})# jsonify message to mantain the data in a json fromat

#create for insert_one in the collection
# with try except to catch some common exceptions
# post is a method form Resource
class Create(Resource):
  def post(self):
    postedData =request.get_json()# geting data as json from request library and pass to as dictionary to postedData
    if postedData and postedData["cred"]["ID"]=="main":#some checking
      try:
        doexist=user.find_one({"name": postedData["data"]["new"]["name"]})
        if not doexist:
            user.insert_one(postedData["data"]["new"])
      except DocumentTooLarge as s:#handing a exception if document is too large for the process that the time outs
        return jsonify({"error":f"{s}"})
      except CollectionInvalid as s:#handing a exception if somehow collection is not there
        return jsonify({"error":f"{s}"})
      except InvalidName as s:#handing a exception if the reffering names are different than the standerd
        return jsonify({"error":f"{s}"})
      except OperationFailure as s:#handing a exception if OPS fail somehow
        return jsonify({"error":f"{s}"})
      else:
        if not doexist:
            return jsonify({"data":"Created new with name {0}".format(postedData["data"]["new"]["name"])})#every thing OK then send Aknowledgment
        else:
            return jsonify({"caution":"no duplicate allowed"})
    else:
      return jsonify({"message":"wrong creds pleas try again"})#wrong cred normal check

class Dump():
    def __init__(self):
        import json
        with open('d2.json') as f:
            file_data = json.load(f)
        user.insert_many(file_data)

#1. `/count_discounted_products`: How many products have a discount on them?
class Dump1(Resource):
    def get(self):# comparing if '$regular_price_value' > '$offer_price_value' that is discount
        try:
            x=user.find({'$expr':{'$gt':['$regular_price_value','$offer_price_value']}}).count()
        except Exception as e:
            return jsonify({"data":f"{e}"})
        else:
            return jsonify({"data":f"{x}"})
#2. `/list_unique_brands`: How many unique brands are present in the collection?
class Dump2(Resource):
    def get(self):#find distinct in 'brand_name'
        try:
            x=user.distinct('brand_name')
        except Exception as e:
            return jsonify({"data":f"{e}"})
        else:
            return jsonify({"data":f"{x}"})
#3. `/count_high_offer_price`: How many products have offer price greater than 300?
class Dump3(Resource):
    def get(self):#comparing if '$offer_price_value' > 300
        try:
            x=user.find({'offer_price_value' : {'$gt' : 300 }}).count()
        except Exception as e:
            return jsonify({"data":f"{e}"})
        else:
            return jsonify({"data":f"{x}"})
#4. `/count_high_discount`: How many products have discount % greater than 30%?
class Dump4(Resource):
    def get(self):#comparing if '$regular_price_value'-'$offer_price_value' > 0.3,'$regular_price_value' (for thirt percent) and count if yes
        try:
            x=user.find({'$expr':{'$gt':[{'$subtract':['$regular_price_value','$offer_price_value']},{'$multiply':[0.3,'$regular_price_value']}]}}).count()
        except Exception as e:
            return jsonify({"data":f"{e}"})
        else:
            return jsonify({"data":f"{x}"})


class Createmulti(Resource):
  def post(self):
    postedData =request.get_json()# geting data as json from request library and pass to as dictionary to postedData
    if postedData and postedData["cred"]["ID"]=="main":#some checking
      try:
            user.insert_many(postedData["data-multi"])
      except DocumentTooLarge as s:#handing a exception if document is too large for the process that the time outs
        return jsonify({"error":f"{s}"})
      except CollectionInvalid as s:#handing a exception if somehow collection is not there
        return jsonify({"error":f"{s}"})
      except InvalidName as s:#handing a exception if the reffering names are different than the standerd
        return jsonify({"error":f"{s}"})
      except OperationFailure as s:#handing a exception if OPS fail somehow
        return jsonify({"error":f"{s}"})
      else:
        return jsonify({"data":"Created new with name {0}".format(postedData["data-multi"])})#every thing OK then send Aknowledgment
    else:
      return jsonify({"message":"wrong creds pleas try again"})#wrong cred normal check


#Update for update_one in the collection
#with try except to catch some common exceptions
#put is a method form Resource

class Update(Resource):
  def put(self):
    postedData =request.get_json()
    if postedData and postedData["cred"]["ID"]=="main":
      try:
        doexist=user.find_one({"name": postedData["data"]["new"]["name"]})
        if doexist:
            user.update_one({"name":postedData["data"]["new"]["name"]},{'$set':postedData["data"]["set"]})#calling update_one to match the name and update the content where name is postedData["data"]["new"]["name"]
      except CollectionInvalid as s:#handing a exception if somehow collection is not there
        return jsonify({"error":f"{s}"})
      except InvalidName as s:#handing a exception if the reffering names are different than the standerd
        return jsonify({"error":f"{s}"})
      except OperationFailure as s:#handing a exception if OPS fail somehow
        return jsonify({"error":f"data not found {s}"})
      else:
        if doexist:
            return jsonify({"data":"Updated where name {0} {1}".format(postedData["data"]["new"]["name"],postedData["data"]["set"])})#every thing OK then send Aknowledgment
        else:
            return jsonify({"data":"not found {0} in first-place".format(postedData["data"]["new"]["name"])})
    else:
      return jsonify({"message":"wrong creds pleas try again"})

#Read for find_one in the collection
#with try except to catch some common exceptions
#post is a method form Resource

class Read(Resource):
  def get(self):
    postedData =request.get_json()
    if postedData and postedData["cred"]["ID"]=="main":
      try:
        documents = user.find_one({"name": postedData["data"]["new"]["name"]})
      except CollectionInvalid as s:#handing a exception if somehow collection is not there
        return jsonify({"error":f"{s}"})
      except InvalidName as s:#handing a exception if the reffering names are different than the standerd
        return jsonify({"error":f"{s}"})
      except OperationFailure as s:#handing a exception if OPS fail somehow
        return jsonify({"error":f"{s}"})
      else:
        if documents:
            return jsonify({"data":"found where {0} {1}".format(postedData["data"]["new"]["name"],documents)})#every thing OK return the documents as the result of find_one
        else:
            return jsonify({"data":"not found {0}".format(postedData["data"]["new"]["name"])})
    else:
      return jsonify({"message":"wrong creds pleas try again"})

#Delete for delete_one in the collection
#with try except to catch some common exceptions
#delete is a method form Resource

class Delete(Resource):
  def delete(self):
    postedData =request.get_json()
    if postedData and postedData["cred"]["ID"]=="main":
      myquery = { "name": postedData["data"]["new"]["name"]}
      try:
        doexist=user.find_one({"name": postedData["data"]["new"]["name"]})
        if doexist :
            user.delete_one(myquery)
      except CollectionInvalid as s:#handing a exception if somehow collection is not there
        return jsonify({"error":f"{s}"})
      except InvalidName as s:#handing a exception if the reffering names are different than the standerd
        return jsonify({"error":f"{s}"})
      except OperationFailure as s:#handing a exception if OPS fail somehow
        return jsonify({"error":f"{s}"})
      else:
        if doexist :
            return jsonify({"data":"deleted where {0}".format(postedData["data"]["new"]["name"])})#every thing OK then send Aknowledgment
        else:
            return jsonify({"data":"not found {0} in first-place".format(postedData["data"]["new"]["name"])})
    else:
      return jsonify({"message":"wrong creds pleas try again"})

#binding resource to Delete -> /delete
api.add_resource(Delete,'/delete')
#binding resource to Read  ->  /read
api.add_resource(Read,'/read')
#binding resource to Update   ->  /update
api.add_resource(Update,'/update')
#binding resource to Create  ->  /create
api.add_resource(Create,'/create')
#binding resource to Createmulti  ->  /create-multi
api.add_resource(Createmulti,'/create-multi')
#created these differenturl as to prevent post collision in create,create-multi and it make naming easy to demonstrate
#binding resource to Message  ->  /
api.add_resource(Message,'/')
#binding resource to Dump1  ->  /count_discounted_products
api.add_resource(Dump1,'/count_discounted_products')
#binding resource to Dump2  ->  /list_unique_brands
api.add_resource(Dump2,'/list_unique_brands')
#binding resource to Dump3  ->  /count_high_offer_price
api.add_resource(Dump3,'/count_high_offer_price')
#binding resource to Dump4  ->  /count_high_discount
api.add_resource(Dump4,'/count_high_discount')



#making the module executable
if __name__=="__main__":
    Dump()#created it because the process mongoimport was not working properly and was indefinitly running
    app.run(host='0.0.0.0',port=5000,debug=True)# running and exposing at some host and port
