import dictdatabase as DDB

DDB.config.storage_directory = "src/database"
DDB.config.use_compression = True

users_dict = {
   "u1": { "name" : "Ben", "age": 30, "job": "Software Engineer" },
   "u2": { "name" : "Sue", "age": 21, "job": "Architect" },
   "u3": { "name" : "Joe", "age": 50, "job": "Manager" },
}
DDB.at("users").create(users_dict)
