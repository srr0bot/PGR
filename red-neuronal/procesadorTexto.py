from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class TextPreprocessor:
    def __init__(self, num_words=10000, oov_token="<OOV>", padding_type='post', maxlen=100):
        self.tokenizer = Tokenizer(num_words=num_words, oov_token=oov_token)
        self.maxlen = maxlen
        self.padding_type = padding_type

    def fit_texts(self, texts):
        self.tokenizer.fit_on_texts(texts)
    
    def get_word_index(self):
        return self.tokenizer.word_index

    def texts_to_sequences(self, texts):
        return self.tokenizer.texts_to_sequences(texts)

    def pad_sequences(self, sequences):
        return pad_sequences(sequences, maxlen=self.maxlen, padding=self.padding_type)
