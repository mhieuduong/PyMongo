# PyMongo

Học cách sử dụng thư viện pymongo
Tìm hiểu các khái niệm của NoSQL nói chung.
Sử dụng thư viện pymongo, thực hiện đủ 4 chức năng CRUD đối với 1 collection. Cấu trúc collection tùy chọn
PyMongo 4.1.1 Documentation — PyMongo 4.1.1 documentation

client = pymongo.MongoClient("mongodb+srv://mhieu:m0ng0Data@cluster0.8dhnaue.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.test

{'$and': [{'$or': [{'category_code': 'web'}, {'category_code': 'social'}]}, {'founded_year': 2004}]}, 
{'$and': [{'$or': [{'category_code': 'web'}, {'category_code': 'social'}]}, {'founded_month': 10}]}


db.trips.find({ "$expr": { "$eq": [ "$end station id", "$start station id" ] } }).count()

db.companies.find({ "$expr": { "$eq": [ "$permalink", "$twitter_username" ] } })

({ "$expr": {"$and": [ {"id_student": "69dctm400"}, { "$gt": [ "$array[0]", 5 ] } ]} })
