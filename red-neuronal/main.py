from cargarRecetas import RecipeDataLoader
from procesadorTexto import TextPreprocessor
from model import RecipeModel
from recipeGenerator import RecipeGenerator

def main():
    data_loader = RecipeDataLoader()
    preprocessor = TextPreprocessor()
    model = RecipeModel()
    generator = RecipeGenerator(model)

    # Cargar y preparar datos
    data = data_loader.load_data('../flask-server/responses.json')
    ingredients, procedures = data_loader.parse_data(data)
    inputs, labels = preprocessor.prepare_sequences(ingredients, procedures)

    # Construir y entrenar el modelo
    model.build_model(vocab_size=10000, embedding_dim=256, rnn_units=128)
    model.train(inputs, labels, epochs=10)

    # Generar nueva receta
    seed_text = "1 taza de harina"
    generated_recipe = generator.generate(seed_text, 100)
    print(generated_recipe)

if __name__ == "__main__":
    main()
