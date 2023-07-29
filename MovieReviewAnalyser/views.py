from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps

from MovieReviewAnalyser.models import *
from MovieReviewAnalyser.getmovie import *
from MovieReviewAnalyser.apps import *
import math



# Create your views here.
def home(request):
    return render(request, "index.html")



@csrf_exempt
def predict(request):
    if request.method == "POST":
        model = apps.get_app_config('MovieReviewAnalyser').model
        processor = apps.get_app_config('MovieReviewAnalyser').processor

        movie = request.POST.get("res")

        review, movie_name, imdb_rating = GetMovie(movie)

        if isinstance(review,list):
            X = processor.pre_process(review)

            result = model.predict(X)

            result = sum(result)/len(result)

            sigmoid = lambda x: 1 / (1 + math.exp(-x))

            review_rating = round((sigmoid(result) * 9) + 1,2)

            if result > 0.7:
                message = "The movie is Good"
            elif result > 0.4:
                message = "The movie is Neutral"
            else:
                message = "The movie is Bad"
        else:
            message = review  
            review_rating = "-"

        data = {
            "message": message,
            "movie_name": movie_name,
            # "imdb_rating": imdb_rating,
            "review_rating": review_rating,
        }


        return  JsonResponse(data)
    else:
        return render(request, "index.html")