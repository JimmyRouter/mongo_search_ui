import pymongo
import collections
from django.http import HttpRequest
from bson.objectid import ObjectId

def get_collections_tree(client: pymongo.MongoClient):
    return {db:client[db].list_collection_names() for db in client.list_database_names() if db not in ['admin', 'config', 'local']}

PI = 3.14159
R = 50
cl = pymongo.MongoClient('127.0.0.1', 27100)
menu_data = get_collections_tree(cl)
db0, col0 = list(menu_data.items())[0][0], list(menu_data.items())[0][1][0]
cllctn_default = cl[db0][col0]
preview_default = list(cllctn_default.find(limit=100))

def make_find_query(req:HttpRequest):
    query_list = []
    if req.method == 'POST':
        req_items = req.POST.items()
    elif req.method == 'GET':
        req_items = req.GET.items()
    for key, value in req_items:
        if value:
            match key:
                case 'csrfmiddlewaretoken':
                    continue
                case 'age':
                    q = {key:{"$gte": int(value)}}
                case _:
                    q = {key: {"$regex": str(value), "$options": "i"}}
            query_list.append(q)
    return {"$and": query_list}


def connect_mongodb(dbname: str, collection_name: str):
    cl = pymongo.MongoClient('127.0.0.1',27100)
    db = cl[dbname]
    return db[collection_name]


def split_list_of_dicts(unsorted_list, key_name):
    splited = collections.defaultdict(list)
    for item in unsorted_list:
        splited[item[key_name]].append(item)
    splited_list = list(splited.values())
    return splited_list


def group_by_family(collection:pymongo.collection.Collection):
    aggregated = collection.aggregate([
        {"$group":{
            "_id":{"h_name":"$father_name", "h_surname": "$father_surname"},
            "ammount of relatives of head":{"$sum":1},
            "members":{"$push":"$$ROOT",
                       },
                  },
        },
        {"$sort": {"_id": 1}},
    ])

    fam_list =[]
    for fam in list(aggregated):
        hed = ' '.join((fam['_id']['h_name'], fam['_id']['h_surname']))
        membs = fam['members']
        fam_dict = {hed:membs}
        fam_list.append(fam_dict)

    return fam_list

def group_by_family_find(collection:pymongo.collection.Collection, query:dict):

    aggregated = collection.aggregate([
        {"$match":query},
        {"$group":{
            "_id":{"h_name":"$father_name", "h_surname": "$father_surname"},
            "ammount of relatives of head":{"$sum":1},
            "members":{
                "$push":"$$ROOT",
            },
        }
    }])

    fam_list =[]
    for fam in list(aggregated):
        hed = ' '.join((fam['_id']['h_name'], fam['_id']['h_surname']))
        membs = fam['members']
        fam_dict = {hed:membs}
        fam_list.append(fam_dict)

    return fam_list

def change_citizen(collection:pymongo.collection.Collection, citiz_id:str, new_info:dict):
    print('CHANGE CITIZEN>>>>>', collection,citiz_id,new_info)
    print(collection.find_one(ObjectId(citiz_id)))
    collection.update_one({'_id':ObjectId(citiz_id)},
                          {'$set':new_info})

def get_svg_data(collection:pymongo.collection.Collection):
    citiz_num = collection.estimated_document_count()
    agr = collection.aggregate([{
        "$group":{
            "_id": "$party",
         "party_members":{"$sum":1}
         },
    }
    ])
    party_pie_list=[]
    colors = ["burlywood", "cornflowerblue", "cadetblue", "darkorchid", "firebrick"]
    for piece in agr:
        percentage = piece['party_members']/citiz_num
        stroke_dash_arr = 2*PI*R*percentage, 2*PI*R
        if party_pie_list: rotate = 360*party_pie_list[-1]['percentage'] + party_pie_list[-1]['rotate']
        else: rotate = 0
        party = piece['_id']
        circle ={'party': party,
                 'stroke': stroke_dash_arr,
                 'rotate': rotate,
                 'percentage':percentage,
                 'color': colors.pop(0)
                 }
        party_pie_list.append(circle)
    return party_pie_list





