from app.database.books_to_database import insert_book_docs
from app.database.sentences_to_database import insert_sentences_docs
from app.database.vectors_to_database import insert_vectors_docs
from app.doc2vec_model.train_model_on_db_sentences import train_model
from pymongo import MongoClient

if __name__ == '__main__':
    connection_string = 'mongodb://localhost:27017/'
    client = MongoClient(connection_string)
    book_db = client.book
    
    insert_book_docs(book_db)
    insert_sentences_docs(book_db)
    train_model(book_db)
    insert_vectors_docs(book_db)
    