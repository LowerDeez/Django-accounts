from django.shortcuts import render, HttpResponse
from .models import Article


def article_list(request):
    articles = Article.objects.all()
    return HttpResponse('Work!')
