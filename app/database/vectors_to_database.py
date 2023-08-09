from pymongo import MongoClient
from random_object_id import generate
from gensim.models import doc2vec
from app.utils.utils import get_word_combinations


def add_vectors_to_db(id_vectors, normed_text_string, collection_vectors, model):
    sentence = normed_text_string.split(' ')
    word_combinations = get_word_combinations(sentence)
    
    for comb in word_combinations:
        value_vec = model.infer_vector(comb)
        vector_doc = {
                'id_vec': generate(),
                'id_vectors': id_vectors,
                'value_vec': value_vec.tolist()
            }
        inserted_id = collection_vectors.insert_one(vector_doc).inserted_id


def insert_vectors_docs(book_db):
    model = doc2vec.Doc2Vec.load('doc2vec_model')
    collection_sentences = book_db.sentences
    collection_vectors = book_db.vectors
    cursor = collection_sentences.find({})
    for document in cursor:
        add_vectors_to_db(document['id_vectors'], document['normed_text_string'], collection_vectors, model)


if __name__ == '__main__':
    connection_string = 'mongodb://localhost:27017/'
    client = MongoClient(connection_string)
    book_db = client.book
    insert_vectors_docs(book_db)