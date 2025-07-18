#pip install azure-core

from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
import requests

# import namespaces
# pip install azure-ai-vision-imageanalysis
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential



def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]
        

        # Authenticate Azure AI Vision client

        # Analyze image
        # Get image captions
        # Get image tags
        # Get objects in the image
        # Get people in the image

                
        # Verificar si el archivo de imagen existe
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"El archivo de imagen '{image_file}' no se encontró.")

        # Authenticate Azure AI Vision client
        print("Autenticando cliente de Azure AI Vision...")
        client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)
        )
        print("Cliente autenticado.")

        # Analyze image
        print(f"Analizando imagen: {image_file}")
        with open(image_file, "rb") as f:
            image_data = f.read()

        # Define las características visuales que deseas analizar
        # Puedes incluir: VisualFeatures.CAPTION, VisualFeatures.TAGS, VisualFeatures.OBJECTS, VisualFeatures.PEOPLE, VisualFeatures.TEXT, VisualFeatures.DENSE_CAPTION
        print("Solicitando análisis con subtítulos, etiquetas, objetos y personas...")
        result = client.analyze(
            image_data=image_data,
            visual_features=[
                VisualFeatures.CAPTION,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
                VisualFeatures.PEOPLE
            ]
        )
        print("Análisis de imagen completado.")

        # Get image captions
        print("\n--- Subtítulos de la imagen ---")
        if result.caption is not None:
            print(f"Subtítulo: '{result.caption.text}' (Confianza: {result.caption.confidence:.2f})")
        else:
            print("No se pudieron generar subtítulos para la imagen.")

        # Get image tags
        print("\n--- Etiquetas de la imagen ---")
        if result.tags is not None:
            if len(result.tags) > 0:
                for tag in result.tags:
                    print(f"Etiqueta: '{tag.name}' (Confianza: {tag.confidence:.2f})")
            else:
                print("No se encontraron etiquetas para la imagen.")
        else:
            print("No se pudieron obtener etiquetas para la imagen.")

        # Get objects in the image
        print("\n--- Objetos en la imagen ---")
        if result.objects is not None:
            if len(result.objects) > 0:
                for obj in result.objects:
                    print(f"Objeto: '{obj.name}' (Confianza: {obj.confidence:.2f})")
                    # Puedes acceder a obj.bounding_box para obtener las coordenadas del objeto
            else:
                print("No se encontraron objetos en la imagen.")
        else:
            print("No se pudieron obtener objetos para la imagen.")

        # Get people in the image
        print("\n--- Personas en la imagen ---")
        if result.people is not None:
            if len(result.people) > 0:
                for person in result.people:
                    print(f"Persona detectada (Confianza: {person.confidence:.2f})")
                    # Puedes acceder a person.bounding_box para obtener las coordenadas de la persona
            else:
                print("No se encontraron personas en la imagen.")
        else:
            print("No se pudieron obtener personas para la imagen.")

    except FileNotFoundError as ex:
        print(f"Error: {ex}")
    except ValueError as ex:
        print(f"Error de configuración: {ex}")
    except Exception as ex:
        print(f"Ocurrió un error: {ex}")



def show_objects(image_filename, detected_objects):
    print ("\nAnnotating objects...")

    # Prepare image for drawing
    image = Image.open(image_filename)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for detected_object in detected_objects:
        # Draw object bounding box
        r = detected_object.bounding_box
        bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height)) 
        draw.rectangle(bounding_box, outline=color, width=3)
        plt.annotate(detected_object.tags[0].name,(r.x, r.y), backgroundcolor=color)

    # Save annotated image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    objectfile = 'objects.jpg'
    fig.savefig(objectfile)
    print('  Results saved in', objectfile)


def show_people(image_filename, detected_people):
    print ("\nAnnotating objects...")

    # Prepare image for drawing
    image = Image.open(image_filename)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for detected_person in detected_people:
        if detected_person.confidence > 0.2:
            # Draw object bounding box
            r = detected_person.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
            draw.rectangle(bounding_box, outline=color, width=3)

    # Save annotated image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    peoplefile = 'people.jpg'
    fig.savefig(peoplefile)
    print('  Results saved in', peoplefile)


if __name__ == "__main__":
    main()
