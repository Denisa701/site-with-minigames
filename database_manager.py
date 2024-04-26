import pymongo
import gridfs
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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

#Conecting to the colection
database=client["WebDev_3Dupb"]
fs = gridfs.GridFS(database)

#creating a table
# userCollection = database["users"]

#adding one user
# user={"username":"misskitty", "password":"MiauBauPwp"}
# userID=userCollection.insert_one(user)
# print(userID.inserted_id)

# creating a list of users
# userList=[
#     {"username":"misskitty","email":"deni.dumitrescu@gmail.com", "password":"MiauBauPwp", "userID":111},
#     {"username":"me_sorry","email":"deni.dumitrescu@gmail.com", "password":"MiauBauPwp", "userID":112},
#     {"username":"how_loud_can_you_cry","email":"deni.dumitrescu@gmail.com", "password":"MiauBauPwp", "userID":113},
#     {"username":"KittysHeaven","email":"deni.dumitrescu@gmail.com", "password":"MiauBauPwp", "userID":114},
#     {"username":"some_name","email":"deni.dumitrescu@gmail.com", "password":"MiauBauPwp", "userID":115}
# ]

# userIds = userCollection.insert_many(userList)
# # print(userIds)

gamesCollection = database["games"]
gameList=[
    {"title":"Ballon Madness","description":"Beat your friend in masuring ballons","image":"","gameID":1},
    {"title":"Endless Runner","description":"Run till you cant anymore","image":"","gameID":2},
]


try:
    file1 = open("ballons.jpeg","rb") # citesc binar pt ca asa merge mongoDB
    content1 = file1.read()
    out1 = fs.put(content1, filename="ballons.jpeg")
    gameList[0]["image"] = out1
    try:
        file2 = open("runner.jpeg","rb") # citesc binar pt ca asa merge mongoDB
        content2 = file2.read()
        out2 = fs.put(content2, filename="runner.jpeg")
        gameList[1]["image"] = out2

        gameIds = gamesCollection.insert_many(gameList)

        highscoresCollection = database["scores"]
        highscoresList = [
            {"gameID":gameList[0]["_id"] , "userID":112, "score":123},
            {"gameID":gameList[0]["_id"] , "userID":114, "score":64},
            {"gameID":gameList[1]["_id"] , "userID":112, "score":76},
            {"gameID":gameList[1]["_id"] , "userID":111, "score":73},
            {"gameID":gameList[0]["_id"] , "userID":113, "score":132},
            {"gameID":gameList[1]["_id"] , "userID":114, "score":42}
        ]
        highScoresIds = highscoresCollection.insert_many(highscoresList)
    except:
        print("error uploading the image 2")
except:
    print("error uploading the image 1")

# uploading the image procedure
# try:
#     file = open("ballons.jpeg","rb") # citesc binar pt ca asa merge mongoDB
#     content = file.read()
#     out = fs.put(content,filename="ballons.jpeg")

    #downloading the image procedure
    # try:
    #     out2 = fs.get(out)
    #     file2 = open("ballons2.jpeg","wb")
    #     byteArray = out2.read()
    #     file2.write(byteArray)
    # except:
    #     print("error downloading the image")
# except:
#     print("error uploading the image")