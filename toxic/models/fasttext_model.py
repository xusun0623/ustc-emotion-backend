import fasttext


class FastText:
    def __init__(self, config, train=True):
        self.model_path = config.model_path
        if train:
            self.classifier = fasttext
        else:
            self.classifier = fasttext.load_model(self.model_path)
        self.train_file = config.train_file
        self.test_file = config.test_file
        self.dev_file = config.dev_file
        self.lr = config.lr
        self.dim = config.embedding_dim
        self.epoch = config.epoch
        self.word_ngrams = config.ngrams
        self.loss = config.loss_function
        self.minCount = config.minCount
        self.bucket = config.bucket

    def predict(self, question):
        """

        :param question:str, 词之间用空格分开
        :return:
        """
        result = self.classifier.predict([question])
        return result[0][0][0]


