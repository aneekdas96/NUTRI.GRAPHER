import gensim
import os
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
import re
from sklearn.decomposition import PCA
import pickle
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# globals
bad_patterns = [r'&.*;', r'[0-9].*']
stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
cur_dir = os.getcwd()
list_of_files = os.listdir(cur_dir)
bad_chars = ['.', '"', ',', '(', ')', '!', '?', ';', ':']

pca_model = pickle.load(open('./server_assets/pca_model.p', 'rb'))
main_doc_vector = pickle.load(open('./server_assets/document_vectors.p', 'rb'))
store = np.array(pickle.load(open('./server_assets/reduced_doc_vectors.p', 'rb')),dtype=np.float32)
d2v_model = gensim.models.doc2vec.Doc2Vec.load('./server_assets/doc2vec.model')

# fetching the labels
def fetch_labels():
    labels = []
    for doc in list_of_files:
        if '.txt' in doc:
            labels.append(doc)
    return labels


# fetching the data associated to each label
def get_training_data(labels):
    training_data = []

    for label in labels:
        path_of_doc = str(cur_dir) + '\\' + str(label)
        f = open(path_of_doc)
        recipe = f.read()
        training_data.append(recipe)
    print('length of training data : ', len(training_data))
    print('training data : ', training_data)
    return training_data


# removing stop words and bad characters
# lemmatizing and stemming words
# removing bad strings and garbage data
def clean_data(training_data):
    for index, recipe in enumerate(training_data):
        filtered_recipe = []
        words_recipe = word_tokenize(recipe)
        for word in words_recipe:
            if word not in stopwords and word not in bad_chars:
                word = stemmer.stem(word)
                word = lemmatizer.lemmatize(word)
                for pattern in bad_patterns:
                    word = re.sub(pattern, '', word)
                filtered_recipe.append(word)
        filtered_recipe = ' '.join(filtered_recipe)
        training_data[index] = filtered_recipe
    return training_data


# data generator to throw a gensim object one at a time
class LabeledLineSentence(object):
    def __init__(self, training_data, labels):
        self.labels_list = labels
        self.doc_list = training_data

    def __iter__(self):
        for index, doc in enumerate(self.doc_list):
            yield gensim.models.doc2vec.LabeledSentence(doc, [self.labels_list[index]])


#############################################################
##########################TRAINING PHASE#####################
#############################################################

def train_model(training_data, labels):
    res = LabeledLineSentence(training_data, labels)
    model = gensim.models.Doc2Vec(size=20, window=10, min_count=0, alpha=0.025, min_alpha=0.025, workers=2)
    model.build_vocab(res)

    # training of model
    for epoch in range(100):
        print('iteration' + str(epoch + 1))
        model.train(res, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.002
        model.min_alpha = model.alpha
    # model.train(res, total_examples=model.corpus_count, epochs=model.iter)

    # saving the created model
    model.save('./server_assets/doc2vec.model')
    print('successfully saved model')


# labels = fetch_labels()
# training_data = get_training_data(labels)
# training_data = clean_data(training_data)
# train_model(training_data, labels)

###############################################################
#################TESTING PHASE#################################
###############################################################

def clean_test_data(test_data):
    filtered_recipe = []
    words_recipe = word_tokenize(test_data)
    for word in words_recipe:
        if word not in stopwords and word not in bad_chars:
            word = stemmer.stem(word)
            word = lemmatizer.lemmatize(word)
            for pattern in bad_patterns:
                word = re.sub(pattern, '', word)
            filtered_recipe.append(word)
    filtered_recipe = ' '.join(filtered_recipe)
    return filtered_recipe


def get_main_doc_vec():
    main_doc_vector = []
    labels = fetch_labels()
    d2v_model = gensim.models.doc2vec.Doc2Vec.load('./server_assets/doc2vec.model')
    for label in labels:
        f = open(label, 'r')
        data = f.read()
        clean_data = clean_test_data(data)
        f.close()
        f = open(label, 'w')
        f.write(clean_data)
        f.close()
        vec_of_doc = d2v_model.infer_vector(word_tokenize(clean_data), alpha=0.1, min_alpha=0.0001, steps=5)
        main_doc_vector.append(vec_of_doc)
    pickle.dump(main_doc_vector, open('./server_assets/document_vectors.p', 'wb'))


# get_main_doc_vec()

def get_reduced_vectors():
    pca = PCA(n_components=3)
    pca.fit(main_doc_vector)
    reduced_doc_vectors = pca.transform(main_doc_vector)
    pickle.dump(reduced_doc_vectors, open('./server_assets/reduced_doc_vectors.p', 'wb'))
    pickle.dump(pca, open('./server_assets/pca_model.p', 'wb'))


# get_reduced_vectors()

def test_model(recipe):
    # pca_model = pickle.load(open('./server_assets/pca_model.p', 'rb'))

    # f = open(recipe, 'r')
    # test_data = f.read()
    # test_data = recipe_text
    test_data = recipe
    test_data = clean_test_data(test_data)
    # f.close()
    vec_of_doc = d2v_model.infer_vector(word_tokenize(test_data), alpha=0.1, min_alpha=0.0001, steps=5)
    reduced_doc_vec = pca_model.transform([vec_of_doc])
    return reduced_doc_vec


def fetch_coor(recipe):
    min_vals = np.min(store, axis=0)
    vec = test_model(recipe)
    vec = vec[-1]
    for index, val in enumerate(vec):
        val = val + abs(min_vals[index])
        val = np.log(val)
        val = val * 3
        vec[index] = val
    return vec


if __name__ == "__main__":

    print(fetch_coor(
        'mix chili powder with rice and leave to cook for 20 minutes. bring to boil. put chicken pieces to get a good stew.'))
