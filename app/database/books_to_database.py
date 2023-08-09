import json
from pymongo import MongoClient
from random_object_id import generate


def insert_book_docs(book_db):
    collection = book_db.book
    data = None
    with open("books.json", "r") as jsonFile:
        data = json.load(jsonFile)
    print(data['1']['contents'])
    for k in data.keys():
        year = None
        try:
            year = int(data[k]['year'])
        except ValueError as e:
            print(e)
            continue
        book_doc = {
            'id_book': generate(),
            'name': data[k]['name'],
            'author': data[k]['author'],
            'publishing': data[k]['publishing'],
            'year': year
        }
        inserted_id = collection.insert_one(book_doc).inserted_id

if __name__ == '__main__':
    connection_string = 'mongodb://localhost:27017/'
    client = MongoClient(connection_string)
    book_db = client.book
    insert_book_docs(book_db)