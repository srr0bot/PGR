import numpy as np

class RecipeGenerator:
    def __init__(self, model, preprocessor):
        self.model = model
        self.preprocessor = preprocessor

    def generate_text(self, seed_text, num_words):
        for _ in range(num_words):
            token_list = self.preprocessor.texts_to_sequences([seed_text])[0]
            token_list = self.preprocessor.pad_sequences([token_list])
            predicted_probs = self.model.model.predict(token_list, verbose=0)
            predicted_index = np.argmax(predicted_probs, axis=-1)[0]
            output_word = ""
            for word, index in self.preprocessor.get_word_index().items():
                if index == predicted_index:
                    output_word = word
                    break
            seed_text += " " + output_word
        return seed_text