import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

class ImageGenerator:
    def __init__(self):
        pass

    def generate_image(self, prompt, ing):
        # Our Host URL should not be prepended with "https" nor should it have a trailing slash.
        os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

        # Paste your API Key below.
        os.environ['STABILITY_KEY'] = 'sk-4N4Sp4UU3RhFsEHOlPz4R1rORMO385qSvWbvFfzYomgkDvpQ'

        # Set up our connection to the API.
        stability_api = client.StabilityInference(
            key=os.environ['STABILITY_KEY'],
            verbose=True,
            engine="stable-diffusion-xl-1024-v1-0"
        )

        print(prompt)
        
        answers = stability_api.generate(
            prompt=f"Imagine that you are a renowned pastry chef, creating an exceptional dessert by generating a single image. Accurately describe all elements, from ingredients ({ing}) to the final presentation, focusing on a single exquisite and detailed image of the dessert. This representation must capture the complete essence of the dessert, its texture, flavor and aroma from its description, ensuring that whoever sees it can almost perceive its flavor. The detailed creation process is as follows: {prompt}",
            seed=1229080980,
            steps=40,
            cfg_scale=5,
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