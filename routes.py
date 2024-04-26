from flask import Flask, jsonify, request
from flask_cors import cross_origin
import pymongo
import gridfs
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import re
from flask_cors import CORS

# <!-- parola mongoBD: DzLVyohfItH9IwCk -->
uri = "mongodb+srv://denisa_dumitrescu:DzLVyohfItH9IwCk@cluster0.icjokml.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Conecting to the colection
database = client["WebDev_3Dupb"]
fs = gridfs.GridFS(database)

# creating a table
userCollection = database["users"]
gamesCollection = database["games"]
highscoresCollection = database["scores"]


app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])

#_______________________________________GET_________________________________________#
# 
@app.route('/getGameID/<game>', methods=['GET'])
@cross_origin(supports_credential=True)
def getGameID(game):
    query = {'title': game}
    document = gamesCollection.find_one(query)
    print(document)

    return jsonify(result=document['gameID'])


# @app.route('/getGameTitle/<gameID>', methods=['GET'])
# @cross_origin(supports_credential=True)
# def getGameTitle(gameID):
#     query = {'_id': gameID}
#     document = gamesCollection.find_one(query)
#     return jsonify(result=document['title'])

@app.route('/getuserID/<user>', methods=['GET'])
@cross_origin(supports_credential=True)
def getuserID(user):
    query = {'username': user}
    document = userCollection.find_one(query)
    print(document)

    return jsonify(result=document['userID'])

@app.route('/getuser/<userID>', methods=['GET'])
@cross_origin(supports_credential=True)
def getuser(userID):
    query = {'userID': int(userID)}
    document = userCollection.find_one(query)
    print(document)

    return jsonify(result=document['username'])


@app.route('/getGameState/<gameID>', methods=['GET'])
@cross_origin(supports_credential=True)
def getGameState(gameID):
    query = {'_id': ObjectId(gameID)}
    result = gamesCollection.find_one(query)
    return jsonify(result=result['gameID'])

# get all scores from the table highscoresCollection
@app.route('/getScores/<gameID>', methods=['GET'])
@cross_origin(supports_credential=True)
def getScores(gameID):
    result = []
    query = {'gameID': ObjectId(gameID)}
    for score in highscoresCollection.find(query):
        result.append({'_id': str(score['_id']), 'gameID':str( score['gameID']),
                      'userID': int(score['userID']), 'score': int(score['score'])})

    # return {'result': result}
    return jsonify(result=result)


#get all scores of a specific minigame
@app.route('/getScoreTable/<gameID>', methods=['GET'])
@cross_origin(supports_credential=True)
def getScoreTable(gameID):

    result = []
    query = {'gameID': ObjectId(gameID)}
    document = highscoresCollection.find(query)
    
    for score in document:
        result.append({ 'gameID':str( score['gameID']), 
                      'userID': int(score['userID']),'score': int(score['score'])})
    for score in result:
        new_query = {'userID': int(score['userID'])}
        new_document = userCollection.find_one(new_query)
        score['userID'] = new_document['username']

    return jsonify(result=result)


#get all the score with the specific mongoDB _id 
@app.route('/getScoresById/<userID>', methods=['GET'])
@cross_origin(supports_credential=True)
def getScoresById(userID):
    query = {'userID': int(userID)}
    document = highscoresCollection.find_one(query)
    return jsonify(result=document['score'])


#get all existing games 
@app.route('/getGames/', methods=['GET'])
@cross_origin(supports_credential=True)
def getGames():

    result = []
    for score in gamesCollection.find():
        result.append({'_id': str(score['_id']), 'title': score['title'], 'description': score['description'], 'image': str(
            score['image']), 'gameID': score['gameID']})

    return jsonify(result=result)


#get the images corresponding with the mongoDB _id
@app.route('/getImageById/<id>', methods=['GET'])
@cross_origin(supports_credential=True)
def getImageById(id):

    out = fs.get(ObjectId(id)) #in the database the id is in ObjectId format, the given parameter is a string so we need to convert it    
    return out.read()

#_______________________________________POST_________________________________________#

@app.route('/login/', methods=['POST'])
@cross_origin(supports_credential=True)
def login():
     # Obținem datele din corpul cererii JSON

    username = request.form.get('username')
    password = request.form.get('password')
    query = {'username': username}
    print(userCollection.find_one(query) == username)

    user = userCollection.find_one(query)

    if user is not None and user['password'] == password:
        message = "Autentificare reușită"
    else:
        message = "Autentificare eșuată"
    return jsonify(message=message)


@app.route('/register/', methods=['POST'])
@cross_origin(supports_credential=True)
def register():
     # Obținem datele din corpul cererii JSON

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    userID = int(111 + userCollection.count_documents({}))

    data ={
        'username' : str(username),
        'password' : str(password),
        'email' : str(email),
        'userID' : int(userID)
    }
    try:
        userCollection.insert_one(data)
        message = "Succesful sign in"
    except:
        message ="Something went wrong"
    return jsonify(message=message)

#_______________________________________POST&PUT_________________________________________#
@app.route('/addScore/', methods=['POST', 'PUT'])
@cross_origin(supports_credential=True)
def addScore():
    requested_id = 0

   
    game_id = request.form.get('gameID')
    user_id = int(request.form.get('userID'))
    score = int(request.form.get('score'))
    print(user_id, game_id)
    
    data = {
        'gameID': ObjectId( game_id),
        'userID': int(user_id),
        'score': int(score)
    }


    query = {'gameID': game_id, 'userID':user_id }

    user = highscoresCollection.find_one(query)
    print(user)

    if request.method == 'POST' and user is None:
        requested_id = highscoresCollection.insert_one(data)

    if request.method == 'PUT' and user is not None:
        requested_id =  highscoresCollection.update_one({'gameID': data['gameID'], 'userID': data['userID']}, {
                                        '$set': {'score':data['score'] }})
   
    return jsonify(id=requested_id)

#_______________________________________PUT_________________________________________#
@app.route('/resetPass/', methods=['PUT'])
@cross_origin(supports_credential=True)
def resetPass():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        userCollection.update_one({'email': email}, {'$set': {'password': password }})
        message = "password reseted succesfully"
    except:
        message ="something went wrong"
    return jsonify(message=message)



if __name__ == "__main__":
    app.run()
