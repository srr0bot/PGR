from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Bidirectional

class RecipeModel:
    def __init__(self):
        self.model = None

    def build_model(self, vocab_size, embedding_dim, rnn_units):
        self.model = Sequential([
            Embedding(vocab_size, embedding_dim),
            Bidirectional(LSTM(rnn_units, return_sequences=True)),
            Bidirectional(LSTM(int(rnn_units/2))),
            Dense(rnn_units, activation='relu'),
            Dense(vocab_size, activation='softmax')
        ])
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    def train(self, X_train, y_train, epochs):
        self.model.fit(X_train, y_train, epochs=epochs)
    
    def summarize(self):
        self.model.summary()
