#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from sklearn import svm, model_selection, metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
import numpy as np
import mylogger

LOGGER = mylogger.getLogger(__name__)


class Classifier():
    def __init__(self, alpha=1e-6, hidden_layer_sizes=(10, 3)):
        self.alpha = alpha
        self.hidden_layer_sizes = hidden_layer_sizes
        # l = list(map(str, list(range(10))))
        # print(self.n_gram(l, 3))

    def gen_features_labels(self):
        LOGGER.info('Start generating data')
        users = []
        file_names = os.listdir('data/male/')
        n_male = len(file_names)
        file_names.extend(os.listdir('data/female/'))
        n_female = len(file_names) - n_male
        cv = CountVectorizer(
            tokenizer=lambda x: x,
            lowercase=False,
            analyzer='word',
            stop_words=None,
            ngram_range=(1, 1),
            max_df=0.2,
            min_df=0.0005,
        )

        for i, file_name in enumerate(file_names):
            sex = 'female'
            if i < n_male:
                sex = 'male'

            with open('data/{}/{}'.format(sex, file_name)) as f:
                users.append(json.loads(f.read()))

        # Features Related to N-gram
        n_n_grams = []
        s_n_grams = []
        d_n_grams = []
        LOGGER.info('Data SIZE(male): {}'.format(n_male))
        LOGGER.info('Data SIZE(female): {}'.format(n_female))
        LOGGER.info('Data SIZE: {}'.format(n_male + n_female))

        for user in users:
            name = list(user['name'])
            n_n_gram = self.n_gram(name, 1)
            n_n_gram.extend(self.n_gram(name, 2))
            n_n_gram.extend(self.n_gram(name, 3))

            s_name = list(user['screen_name'])[1:]
            s_n_gram = self.n_gram(s_name, 1)
            s_n_gram.extend(self.n_gram(s_name, 2))
            s_n_gram.extend(self.n_gram(s_name, 3))

            desc = list(user['description'])
            d_n_gram = self.n_gram(desc, 1)
            d_n_gram.extend(self.n_gram(desc, 2))
            d_n_gram.extend(self.n_gram(desc, 3))

            n_n_grams.append(n_n_gram)
            s_n_grams.append(s_n_gram)
            d_n_grams.append(d_n_gram)
        LOGGER.info('Feature: {}'.format(len(n_n_grams)))
        n_n_gram_features = cv.fit_transform(n_n_grams).toarray()
        s_n_gram_features = cv.fit_transform(s_n_grams).toarray()
        d_n_gram_features = cv.fit_transform(d_n_grams).toarray()

        # TODO: Locationをどうする?

        numer_features = []
        for user in users:
            feature = []
            feature.append(int(user['protected']))
            feature.append(np.log10(int(user['followers_count']) + 1))
            feature.append(np.log10(int(user['friends_count']) + 1))
            feature.append(np.log10(int(user['statuses_count']) + 1))

            # リストを持っているかどうか
            if user['listed_count'] != 0:
                feature.append(1)
            else:
                feature.append(0)

            # 色を変えているかどうか 通常1DA1F2
            if user['profile_link_color'] != '1DA1F2':
                feature.append(1)
            else:
                feature.append(0)

            if user['profile_sidebar_border_color'] != 'C0DEED':
                feature.append(1)
            else:
                feature.append(0)

            feature.append(int(user['contributors_enabled']))
            feature.append(int(user['is_translator']))
            feature.append(int(user['is_translation_enabled']))
            feature.append(int(user['profile_use_background_image']))
            feature.append(int(user['has_extended_profile']))
            feature.append(int(user['default_profile']))
            feature.append(int(user['default_profile_image']))
            numer_features.append(feature)

        LOGGER.info("Finish n-gram")
        self.features = np.c_[
            n_n_gram_features,
            s_n_gram_features,
            d_n_gram_features,
            numer_features,
        ]

        self.labels = [
            0 if i < n_male else 1
            for i in range(n_male + n_female)
        ]
        LOGGER.info('Feature Dimension: {}'.format(len(self.features[0])))
        LOGGER.info('Finish generating data')

    def n_gram(self, lst, n, delim=" "):
        return [delim.join(
                    (["<s>"] * (n - 1) + lst + ["</s>"] * (n - 1))[i: i + n]
                ) for i in range(len(lst) + n - 1)]

    def train(self):
        # self.clf = svm.LinearSVC()
        self.clf = MLPClassifier(
            alpha=1e-5,
            hidden_layer_size=(1000, 3),
            random_state=0
        )
        self.clf.fit(self.features, self.labels)

    def eval(self):
        LOGGER.info('Start evaluation')
        # self.clf = svm.LinearSVC(C=1)
        self.clf = MLPClassifier(
            alpha=self.alpha,
            hidden_layer_sizes=self.hidden_layer_sizes,
            random_state=0
        )
        features_train, features_test, labels_train, labels_test = \
            model_selection.train_test_split(self.features,
                                             self.labels,
                                             test_size=0.2,
                                             random_state=0)

        LOGGER.info('Start fitting')
        self.clf.fit(features_train, labels_train)
        LOGGER.info('Finish fitting')
        LOGGER.info('Start prediction')
        predicted_labels = self.clf.predict(features_test)
        LOGGER.info('Finish prediction')
        score = metrics.accuracy_score(labels_test, predicted_labels)
        print('# Accuracy Score')
        print(score)
        LOGGER.info('Finish evaluation')

    def store_dump(self):
        LOGGER.info('Start creating dump')
        joblib.dump(self.features, 'dump/features.pkl')
        joblib.dump(self.labels, 'dump/labels.pkl')
        LOGGER.info('Finish creating dump')

    def load_dump(self):
        LOGGER.info('Start loading dump')
        self.features = joblib.load('dump/features.pkl')
        self.labels = joblib.load('dump/labels.pkl')
        LOGGER.info('Finish loading dump')


def grid_search():
    def get_comb(params):
        length = 1
        for v in params.values():
            length *= len(v)
        return length

    def select_params(idx, params):
        ret = {}
        tmp = idx
        for k, v in params.items():
            ret[k] = params[k][tmp % len(v)]
            tmp = int(tmp / len(v))
        return ret

    params = {
            'alpha': [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
            'hidden_layer_sizes': [
                (10, 2),
                (10, 3),
                (10, 4),
                (20, 2),
                (20, 3),
                (20, 4),
            ],
            }
    length = get_comb(params)

    print('\t'.join(params.keys()))
    for i in range(length):
        selected_params = select_params(i, params)
        print(selected_params)
        clf = Classifier(
            alpha=selected_params['alpha'],
            hidden_layer_sizes=selected_params['hidden_layer_sizes']
        )
        output = list(selected_params.values())
        print('\t'.join(list(map(str, output))))
        # clf.gen_features_labels()
        clf.load_dump()
        clf.eval()


def main():
    clf = Classifier()
    clf.gen_features_labels()
    # clf.store_dump()
    # clf.eval()
    # grid_search()


if __name__ == "__main__":
    main()
