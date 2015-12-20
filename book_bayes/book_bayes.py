# coding: utf-8

from collections import Counter


class BookClassify(object):
    """
    使用朴素贝叶斯算法做图书分类
    reference: http://www.jianshu.com/p/f6a3f3200689
    跑单元测试 python -m doctest -v book_bayes.py

    >>> book_classify = BookClassify()
    >>> book_classify.classify(['毛姆', '英国文学', '小说', '英国'])
    'humanities'
    >>> book_classify.classify(['数学', '计算机', '科普', '吴军'])
    'computer'
    """

    def __init__(self):
        self.load_data()
        self.calc_book_probability()
        self.computer_tag_probability_mapper = self.calc_tag_probability_mapper(self.all_computer_tags)
        self.humanities_tag_probability_mapper = self.calc_tag_probability_mapper(self.all_computer_tags)

    def load_data(self):
        self.all_computer_tags = []
        self.all_humanities_tags = []
        self.all_tags = []
        self.all_labels = []

        with open('book-new.csv', 'r') as csvfile:
            raw_data = csvfile.readlines()

        for line in raw_data:
            line_list = line.strip().split(',')
            tags_list = line_list[:-2]
            label = line_list[-1]

            if label == '1':
                self.all_computer_tags.extend(tags_list)
            else:
                self.all_humanities_tags.extend(tags_list)
            self.all_tags.extend(tags_list)
            self.all_labels.append(label)
        self.all_tags = list(set(self.all_tags))

    def calc_book_probability(self):
        self.computer_classify_probability = len([i for i in self.all_labels if i == '1']) / float(len(self.all_labels))
        self.humanities_classify_probability = 1 - self.computer_classify_probability

    def calc_tag_probability_mapper(self, classify_tags):
        classify_tags_mapper = Counter(classify_tags)
        tags_count = float(sum(classify_tags_mapper.values()))
        tags_mapper = {
            i: classify_tags_mapper.get(i, 0) / tags_count
            for i in self.all_tags
        }
        return tags_mapper

    def calc_classify_probability(self, tags, probability_mapper, classify_probability):
        probalility_list = [probability_mapper.get(i, 1) for i in tags]
        if len(probalility_list) == sum(probalility_list):
            return 0

        tags_probability = reduce(lambda x, y: x * y, probalility_list)
        classify_probability = tags_probability * classify_probability
        return classify_probability

    def classify(self, tags):
        computer_probability = self.calc_classify_probability(
            tags,
            self.computer_tag_probability_mapper,
            self.computer_classify_probability
        )
        humanities_probability = self.calc_classify_probability(
            tags,
            self.humanities_tag_probability_mapper,
            self.humanities_classify_probability
        )
        classify = 'computer' if computer_probability > humanities_probability else 'humanities'
        return classify
