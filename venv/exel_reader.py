import pandas
import pymongo
import collections
import datetime

from pymongo.errors import InvalidName

xls_filename = 'Voter_list/Voter_fixed.xlsx'
parse_cfg={
           'name':[4,str],
           'surname':[14,str],
           'father_name':[5,str],
           'gender':[8,str],
           'age':[7,int],
           'address':[6,str],
           'section':[10,str],
           'polling_station':[11,str],
           'constituency':[13,str],
           'grouping':[15,str],
           'master_group':[16,str],
           'age_group':[17,str],
           'district':[18,str],
           }

add_fields ={
    'phone':910000000000,
    'party':'0',
    'profession':'0',
    'familyID':'0',
    'remarks': {
        'promised':'0',
        'questionary':'0',
        'remark':'0',
    },
}


def split_list_of_dicts(unsorted_list,key_name):
    splited = collections.defaultdict(list)
    for item in unsorted_list:
        splited[item[key_name]].append(item)
    splited_list = list(splited.values())
    return splited_list


def get_citizens_list(exel_file:str,parsing_config:dict[str:list],additional_fields:dict)->list:
    parse_cfg = {cfg_key: column for cfg_key, [column, _] in parsing_config.items()}
    enc_cfg = {column: enc_type for column, enc_type in parsing_config.values()}
    xls_readed_raw = pandas.read_excel(exel_file, usecols=list(range(19)), header=0, dtype=enc_cfg, verbose=True)
    dicts_list =[]
    for row in xls_readed_raw.iterrows():
        item = []
        lrow = list(row[1]) #taking a single row-->list of row cell values
        for key,column in parse_cfg.items():
            value = lrow[column]
            match key:
                case 'name':
                    value = str(value).split()
                    surname = value.pop(-1)
                    value = ' '.join(value)
                    # item.append(('father surname', surname))
                case 'father_name':
                    value = str(value).split()
                    surname = value.pop(-1)
                    value = ' '.join(value)
                    item.append(('father_surname', surname))
                case 'age':
                    dob = 2019 - int(value)
                    value = value+4
                    item.append(('dob', datetime.datetime(dob,1,1)))
            #create list of tuples[(key,value),...]
            key_value = (key, value)
            item.append(key_value)
        #create list of dicts: each dict is citizen
        dict_item = dict(item)
        dict_item.update(additional_fields)
        dicts_list.append(dict_item)
    return dicts_list


def drop_all(client:pymongo.MongoClient):
    db_list = client.list_database_names()
    for db in db_list:
        if not any(db == name for name in ['admin', 'config', 'local']):
            client.drop_database(db)
            print('DB DROPPED>>>',db)

cl = pymongo.MongoClient()
# db = cl[]
if __name__ == '__main__':
    drop_all(cl)
    sikkim_raw = get_citizens_list(exel_file=xls_filename,parsing_config=parse_cfg,additional_fields=add_fields)
    for cnstncy in split_list_of_dicts(sikkim_raw,'constituency'):
      sections_list = split_list_of_dicts(cnstncy,'section')
      for insert_batch in sections_list:
        dbname = str(insert_batch[0]['constituency'])
        db_name = ''.join(e for e in dbname if e.isalnum())
        cllctnname = str(insert_batch[0]['section'])
        collection_name = ''.join(e for e in cllctnname if e.isalnum())
        print('batch len>>>',insert_batch.__len__())
        try:
            db = cl[db_name]
            print(collection_name)
            collctn = db[collection_name]
            collctn.insert_many(insert_batch)
            print(collctn.estimated_document_count())

        except InvalidName as e:
            print(e)
            db = cl[db_name]
            collctn = db['Empty_Section']
            collctn.insert_many(insert_batch)
        except Exception as e:
            print(e)
            print('raw dbname>>>',dbname)
            print('stripped db_name>>>',db_name)
            print('raw cllctnname>>>', cllctnname)
            print('stripped collection_name>>>', collection_name)
            print('INSERT BATCH:>>>>', insert_batch[0])
            continue

