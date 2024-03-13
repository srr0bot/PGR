import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
from stability_ai import ImageGenerator

app = Flask(__name__)
CORS(app)

def procesar_respuesta(respuesta):
    lineas = respuesta.strip().split('\n')
    titulo = lineas[0]
    ingredientes_index = next(i for i, linea in enumerate(lineas) if "Ingredientes:" in linea)
    procedimiento_index = next(i for i, linea in enumerate(lineas) if "Procedimiento:" in linea)
    ingredientes = ' '.join(lineas[ingredientes_index:procedimiento_index])
    procedimiento = ' '.join(lineas[procedimiento_index:])
    return titulo, ingredientes, procedimiento

def guardar_receta_desde_respuesta(respuesta, nombre_archivo='responses.json'):
    titulo, ingredientes, procedimiento = procesar_respuesta(respuesta)
    recetas = cargar_recetas(nombre_archivo)
    
    if titulo in recetas:
        print(f"Ya existe una receta con el título '{titulo}'. No se guardará para evitar duplicados.")
    else:
        recetas[titulo] = {
            'ingredientes': ingredientes,
            'procedimiento': procedimiento
        }
        
        with open(nombre_archivo, 'w') as archivo:
            json.dump(recetas, archivo, indent=4)
        
        print(f"La receta '{titulo}' se ha guardado correctamente.")

def cargar_recetas(nombre_archivo='responses.json'):
    try:
        with open(nombre_archivo, 'r') as archivo:
            recetas = json.load(archivo)
    except FileNotFoundError:
        recetas = {}
    return recetas

@app.route("/api/openai", methods=["GET", "POST"])

def ObtenerIngredientes():
    datos = request.json
    ingredientes_seleccionados = datos.get("ingredientesSeleccionados")
    nombres_ingredientes = ", ".join(ingredientes_seleccionados.keys())
    print(nombres_ingredientes)
    client = OpenAI()
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            jsonify(
                {"error": "La variable de entorno OPENAI_API_KEY no está configurada."}
            ),
            500,
        )
    else:
        try:
            # Crear la instancia del cliente OpenAI con la clave de la API
            client = OpenAI(api_key=api_key)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"haz una receta (debe ser un postre) con los siguientes ingredientes {nombres_ingredientes} (la estructura es titulo, ingredientes, instrucciones)",
                    }
                ],
            )
            
            response = completion.choices[0].message.content

            titulo, contenido = response.split("Ingredientes:")
            ingredientes, procedimiento = contenido.split("Instrucciones:")
            titulo = titulo.strip()
            ingredientes = ingredientes.strip()
            procedimiento = procedimiento.strip()
            
            respuesta_del_prompt = f"{titulo}\nIngredientes: {ingredientes}\nProcedimiento: {procedimiento}"
            print(respuesta_del_prompt)

            imageGenerator = ImageGenerator()
            imageGenerator.generate_image(prompt=procedimiento, ing=ingredientes)

            receta_dict = {
                "titulo": titulo,
                "ingredientes": ingredientes,
                "procedimiento": procedimiento,
            }

            guardar_receta_desde_respuesta(respuesta_del_prompt)


            return jsonify(receta_dict)
        except OpenAIError as e:
            print(f"Error al inicializar la instancia de OpenAI: {e}")


if __name__ == "__main__":
    app.run(debug=True)