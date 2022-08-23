import logging

from flask_pymongo import pymongo
from flask import jsonify, request


con_string = "mongodb+srv://hemchandhar:hemchandhar@cluster0.gtiu8uf.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('testdb')

user_collection = pymongo.collection.Collection(db, 'users')
print("MongoDB connected Successfully")


def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world'
        print("Hello world")
        return res

    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


   

    @endpoints.route('/read-users',methods=['GET'])
    def read_users():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Retrieved Successfully from the Database."
            }
            output = [{'Name' : user['name'], 'Email' : user['email']} for user in users]   #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/update-users',methods=['PUT'])
    def update_users():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"id":req_body['id']}, {"$set": req_body['updated_user_body']})
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/delete',methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    return endpoints
