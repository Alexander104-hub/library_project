from pymongo import MongoClient

from gensim.models import doc2vec
import pickle
import logging

from app.utils.utils import get_word_combinations

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_sentences(book_db):
    sentences = []
    collection_sentences = book_db.sentences
    cursor = collection_sentences.find({})
    for document in cursor:
        sentences.append(document['normed_text_string'].split(' '))
    return sentences


def get_tagged_doc(sentences: list[list]):
    tagged_doc = []
    for i, sentence in enumerate(sentences):
        tagged_doc.append(doc2vec.TaggedDocument(sentence, [i]))
    return tagged_doc


def train_model(book_db):
    sentences = get_sentences(book_db)
    word_combinations = []
    for sentence in sentences:
        word_combinations += get_word_combinations(sentence)
    tagged_doc = get_tagged_doc(word_combinations)
    model = doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
    model.build_vocab(tagged_doc)
    model.train(tagged_doc, total_examples=model.corpus_count, epochs=model.epochs)
    model.save('doc2vec_model')
    with open('tagged_doc', 'wb') as fp:
        pickle.dump(tagged_doc, fp)
    
    return model, tagged_doc


# model = doc2vec.Doc2Vec.load('doc2vec_model')