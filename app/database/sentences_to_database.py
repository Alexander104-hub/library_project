import json
import re
from nltk.corpus import words, stopwords
import pymorphy2
from nltk.stem.snowball import SnowballStemmer
from pymongo import MongoClient
from random_object_id import generate

stemmer = SnowballStemmer("russian") 
russian_stopwords = stopwords.words("russian")
english_stopwords = stopwords.words('english')

custom_rus_stemmed_stop_words = ['занят', 'модул']

english_words = set(words.words())
morph = pymorphy2.MorphAnalyzer()


def is_valid_word(word):
    if word in english_stopwords or word in russian_stopwords:
        return False
    if word in english_words:
        return True
    else:
        parsed_word = morph.parse(word)[0]
        return parsed_word.is_known

def get_sentence_list(contents):
    split_regex = re.compile(r'[.|!|?|…|\n]')
    sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(contents)])
    return sentences

def get_norm_sentence(sentence):
    sentence = re.findall(r'\b[а-яёa-z]+\b', sentence)
    sentence = [stemmer.stem(word) for word in sentence if is_valid_word(word)]
    sentence = [word for word in sentence if word not in custom_rus_stemmed_stop_words]
    if len(sentence) > 1:
        return sentence
    return None

def add_sentences_to_db(id_book, contents, collection_sentences):
    sentences = get_sentence_list(contents)
    for sentence in sentences:
        sentence_norm = get_norm_sentence(sentence)
        if sentence_norm == None:
            continue
        
        id_vectors = generate()
        sentence_doc = {
                'id_sentence': generate(),
                'id_book': id_book,
                'id_vectors': id_vectors,
                'text_string': sentence,
                'normed_text_string': ' '.join(sentence_norm)
            }
        inserted_id = collection_sentences.insert_one(sentence_doc).inserted_id
    

def insert_sentences_docs(book_db):
    collection_books = book_db.book
    collection_sentences = book_db.sentences
    cursor = collection_books.find({})
    for document in cursor:
        data = None
        with open("books.json", "r") as jsonFile:
            data = json.load(jsonFile)
        for k in data.keys():
            if data[k]['name'] == document['name']:
                add_sentences_to_db(document['id_book'], data[k]['contents'], collection_sentences)



if __name__ == '__main__':
    connection_string = 'mongodb://localhost:27017/'
    client = MongoClient(connection_string)
    book_db = client.book
    insert_sentences_docs(book_db)