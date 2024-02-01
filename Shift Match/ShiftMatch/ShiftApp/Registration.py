import pymongo 

myclient = pymongo.MongoClient("mongodb+srv://user01:WAX5VkFPgLmrclRt@shiftmatch.mux73es.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["ShiftMatch"]
mycol = mydb["users"]

firstName = ""
lastName = ""
email = ""


mydict = { "Firstname": "harman", "Lastname": "dhami" }

x = mycol.insert_one(mydict)