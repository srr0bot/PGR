import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

class ImageGenerator:
    def __init__(self):
        pass

    def generate_image(self, prompt):
        # Our Host URL should not be prepended with "https" nor should it have a trailing slash.
        os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

        # Paste your API Key below.
        os.environ['STABILITY_KEY'] = 'sk-dQozY5O68lathn3lnhHmR4luxR6uMqiDS23VCqG4U1ha0OZY'

        # Set up our connection to the API.
        stability_api = client.StabilityInference(
            key=os.environ['STABILITY_KEY'],
            verbose=True,
            engine="stable-diffusion-xl-1024-v1-0"
        )

        print(prompt)
        
        answers = stability_api.generate(
            prompt=f"Imagina que eres un chef pastelero de renombre, creando un postre excepcional. Describe con precisión todos los elementos, desde ingredientes hasta la presentación final, enfocándote en una sola versión exquisita y detallada del postre. Esta representación deberá capturar la esencia completa del postre, su textura, sabor y aroma a partir de su descripción, logrando que quien la vea pueda casi percibir su sabor. El proceso de creación detallado es el siguiente: {prompt}",
            seed=1229080980,
            steps=70,
            cfg_scale=8.0,
            width=1024,
            height=1024,
            samples=1,
            sampler=generation.SAMPLER_K_DPMPP_2M
        )

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                         "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    ruta = "../client/src/images/"
                    ruta_completa = os.path.join(ruta, str(artifact.seed)+ ".png")
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save(ruta_completa)