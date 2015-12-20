# coding: utf-8

import numpy as np
from collections import Counter


class BookClassify(object):
    """
    使用朴素贝叶斯算法做图书分类
    reference: http://www.jianshu.com/p/f6a3f3200689
    跑单元测试 python -m doctest -v book_bayes.py

    >>> book_classify = BookClassify()
    >>> book_classify.classify(['毛姆', '英国文学', '小说', '英国'])
    'humanities'
    >>> book_classify.classify(['文学', '罗贯中'])
    'humanities'
    >>> book_classify.classify(['数学', '计算机', '科普', '吴军'])
    'computer'
    >>> book_classify.classify(['Python', 'golang', '科学'])
    'computer'
    """

    def __init__(self):
        self.load_data()
        self.calc_book_probability()

    def load_data(self):
        self.all_computer_tags = []
        self.all_humanities_tags = []
        self.all_labels = []

        with open('book-new.csv', 'r') as csvfile:
            raw_data = csvfile.readlines()

        for line in raw_data:
            line_list = line.strip().split(',')
            tags_list = [tag.lower() for tag in line_list[:-2]]
            label = line_list[-1]

            if label == '1':
                self.all_computer_tags.extend(tags_list)
            else:
                self.all_humanities_tags.extend(tags_list)
            self.all_labels.append(label)

    def calc_book_probability(self):
        self.computer_classify_probability = len([i for i in self.all_labels if i == '1']) / float(len(self.all_labels))
        self.humanities_classify_probability = 1 - self.computer_classify_probability

    def calc_tag_probability(self, tag, classify_tags):
        classify_tag_mapper = Counter(classify_tags)
        total_tag_count = float(sum(classify_tag_mapper.values()))
        tag_count = classify_tag_mapper.get(tag, 1)
        tag_probability = tag_count / total_tag_count
        return tag_probability

    def calc_classify_probability(self, tags, classify_tags, classify_probability):
        probalility_list = [self.calc_tag_probability(tag, classify_tags) for tag in tags]
        probalility_list.append(classify_probability)
        classify_probability = sum(np.log(probalility_list))
        return classify_probability

    def classify(self, tags):
        tags = [tag.lower() for tag in tags]
        computer_probability = self.calc_classify_probability(
            tags,
            self.all_computer_tags,
            self.computer_classify_probability
        )
        humanities_probability = self.calc_classify_probability(
            tags,
            self.all_humanities_tags,
            self.humanities_classify_probability
        )
        classify = 'computer' if computer_probability > humanities_probability else 'humanities'
        return classify
