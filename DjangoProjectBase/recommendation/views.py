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

_ = load_dotenv('../openAI.env')
openai.api_key  = os.environ['openAI_api_key']

def recommendation(request):
    return render(request, 'recommendation.html', {})

def submit(request):
    print("ss")
    print('texto')
    # a = request.POST['user_input']
    # print(a)
    searchTerm = request.GET.get('user_input')
    print(searchTerm)
    with open('../movie_descriptions_embeddings.json', 'r') as file:
        file_content = file.read()
        movies = json.loads(file_content)

    # a = call_command('add_embeddings_db')
    req = "pelicula de comedia"
    # req = searchTerm

    emb = get_embedding(req,engine='text-embedding-ada-002')

    sim = []
    for i in range(len(movies)):
        sim.append(cosine_similarity(emb,movies[i]['embedding']))

    sim = np.array(sim)
    idx = np.argmax(sim)
    print(movies[idx]['title'])
    print(movies[idx]['description'])
    print(type(movies))
    
        # if request.method == "POST" :
        #     print("hh")
    # return HttpResponse(movies)
    return render(request, 'recommendation.html', {'movies': movies[idx].values})


# def home(request):
#     searchTerm = request.GET.get('searchMovie')
#     print('buscando')
#     if searchTerm: 
#        movies = Movie.objects.filter(title__icontains=searchTerm) 
#     else: 
#         movies = Movie.objects.all()
#     return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})