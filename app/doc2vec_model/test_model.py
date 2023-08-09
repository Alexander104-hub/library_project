from gensim.models import doc2vec
import pickle

if __name__ == '__main__':
    model = doc2vec.Doc2Vec.load('doc2vec_model')
    inferred_vector = model.infer_vector(['знакомств', 'learn'])
    sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
    data = []
    with open ('tagged_doc', 'rb') as fp:
        data += pickle.load(fp)

    for e, s in enumerate(sims):
        if e >= 50:
            break
        print(data[s[0]], s[1])