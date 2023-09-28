from django.shortcuts import render
from .models import Recommendation
import os
import openai
from dotenv import load_dotenv
from django.core.management import call_command
from django.shortcuts import get_object_or_404, redirect
from dotenv import load_dotenv, find_dotenv
import json
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np
from django.http import HttpResponse
from .forms import TableForm
import requests
from PIL import Image
from io import BytesIO

_ = load_dotenv('../openAI.env')
openai.api_key  = os.environ['openAI_api_key']

def recommendation(request):
    return render(request, 'recommendation.html', {})

def recomendar(request):
    if request.method == "POST":
        form = TableForm(request.POST)  
        if form.is_valid():
            texto = form.cleaned_data['descrp']
            print(texto)

            with open('../movie_descriptions_embeddings.json', 'r') as file:
                file_content = file.read()
                movies = json.loads(file_content)

            emb = get_embedding(texto,engine='text-embedding-ada-002')

            sim = []
            for i in range(len(movies)):
                sim.append(cosine_similarity(emb,movies[i]['embedding']))

            sim = np.array(sim)
            idx = np.argmax(sim)

            #Se hace la conexión con la API de generación de imágenes. El prompt en este caso es:
            #Alguna escena de la película + "nombre de la película"

            # idx_movie = np.random.randint(len(movies)-1)
            # print(movies[idx_movie])
            response = openai.Image.create(
            prompt=f"Alguna escena de la película {movies[idx]['title']}",
            n=1,
            size="256x256"
            )
            image_url = response['data'][0]['url']

            # La API devuelve la url de la imagen, por lo que debemos generar una función auxiliar que
            # descargue la imagen.
            def fetch_image(url):
                response = requests.get(url)
                response.raise_for_status()

                # Convert the response content into a PIL Image
                image = Image.open(BytesIO(response.content))
                return(image)

            img = fetch_image(image_url)
            img.show()
            movies = movies[idx]
            movies['url'] = image_url
            movies['imagen'] = img
            
            # print(movies.keys())
    
            return render(request, 'recommendation.html', {'movies': movies.values})
    else:
        form = TableForm()  
    return render(request,'recommendation.html',{'form':form})