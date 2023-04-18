from itertools import count
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import json
import sys
from django.db.models import Q
from django.db.models import Case, When
import pandas as pd

sys.setrecursionlimit(1500)


def home (request):
    form = CreateUserForm()
    manga = Manga.objects.filter(category = 1)
    # manhua = Manga.objects.filter(category = 'Adventure - Manhua - Truyện Màu')
    context = {
        'mangaList': manga,
        # 'manhuaList' : manhua,
        'form' : form,
    }
    
    if(request.method == 'POST'):
        print("dk")
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            print("dk thanh cong")
            form.save()
    return render(request, 'app/home.html', context)


def register (request):
    form = UserCreationForm()
    context = {
        'form': form
    }
   
    return render(request, 'app/home.html', context)


def Login (request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == 'POST'):
        username = request.POST['txtUsername']
        password = request.POST['txtPassword']
        print(username)
        print(password)
        user = authenticate(request,username = username , password = password)
        print("user",user)
        
        if user is not None:
            login(request, user)
            print("Mk dùng")
        else: messages.info(request, "Tk hoac mat khau khong dung")
            

    return render(request, 'app/base.html')

def logoutPage (request):
    logout(request)

    return redirect('/')


def base (request):

    return render(request, 'app/home.html' )


def manga (request, id):
    
    manga = Manga.objects.get(idManga=id)
    
    chapterList = Chapter.objects.filter(idChapter=id)
    
    listComment = Comment.objects.filter(manga=id)
    
    sum = 0
    
    for item in chapterList:
       sum = sum + item.viewCount
        
    length = chapterList.count()
    
    print(length)
    
    context = {
        'manga': manga,
        'chapterList' : chapterList,
        'length' : length,
        'sum' : sum,
        'listComment' : listComment
    }
    
    if(request.method == 'POST'):
        print(request.body)
        ratting = Myrating(user = request.user , manga = manga , rating = request.POST['ratting'])
        ratting.save()
        
        if(request.POST['comment'] != ''):
            comment = Comment(user = request.user , manga = manga , context = request.POST['comment'])
            comment.save()
            
        
    
    
   
    return render(request, 'app/manga.html' , context)


def chapter (request,mangaId, chapterId):
    chapter = Chapter.objects.filter(idChapter=mangaId , order = chapterId).first()
    chapter.viewCount = chapter.viewCount + 1
    chapter.save()
    chapterAll = Chapter.objects.filter(idChapter=mangaId)
    chapterContent = chapter.content
    chapterNext = chapter.order + 1
    chapterPrev = chapter.order - 1
    print(chapter)
    print(chapterContent)
    context = {
        'manga': manga,
        'chapterList' : chapter,
        'chapterContent' : chapterContent,
        'chapterAll' : chapterAll,
        'chapterNext' : chapterNext,
        'chapterPrev' : chapterPrev,
    }

    return render(request, 'app/chapter.html' , context)

def profile (request):
  
    
    return render(request, 'app/profile.html')


def hot (request):
    manga = Manga.objects.all().order_by('viewCount')[:5]
    
    print(manga)
    
    context = {
        'mangaList' : manga
    }
    
    return render(request, 'app/hot.html' , context)


def favorite (request):
  
    return render(request, 'app/favorite.html')


def new (request):
    manga = Manga.objects.all().order_by('created_at')[:5]
    
    print(manga)
    
    context = {
        'mangaList' : manga
    }
    

    return render(request, 'app/new.html' , context)

def get_similar(movie_name,rating,corrMatrix):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

def recommed (request):
    movie_rating=pd.DataFrame(list(Myrating.objects.all().values()))

    # new_user=movie_rating.user_id.unique().shape[0]
    # current_user_id= request.user.id
	# if new user not rated any movie
    # if current_user_id>new_user:
    #     movie=Manga.objects.get(idManga= ma)
    #     q=Myrating(user=request.user,movie=movie,rating=0)
    #     q.save()

    print(movie_rating)
    userRatings = movie_rating.pivot_table(index=['user_id'],columns=['manga_id'],values='rating')
    userRatings = userRatings.fillna(0,axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(Myrating.objects.filter(user=request.user).values())).drop(['user_id','id'],axis=1)
    user_filtered = [tuple(x) for x in user.values]
    movie_id_watched = [each[0] for each in user_filtered]

    similar_movies = pd.DataFrame()
    for movie,rating in user_filtered:
        similar_movies = similar_movies.append(get_similar(movie,rating,corrMatrix),ignore_index = True)

    movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
    movies_id_recommend = [each for each in movies_id if each not in movie_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
    movie_list=list(Manga.objects.filter(idManga__in = movies_id_recommend).order_by(preserved)[:10])

    context = {'movie_list': movie_list}
  
    return render(request, 'app/recommed.html' , context)



def search (request):
    print(request.body)
    keyword = request.POST['txtSearch']
    qs = Manga.objects.all()
    for term in keyword.split():
        qs = qs.filter( Q(name__icontains = term))
   
    print(qs)
    
    result = []
    
    for item in qs:
        result.append(Manga.objects.get(idManga = item))
        print("item" , item)
        
    # mangaList = Manga.objects.get(idManga = item)
    # print("manga" , manga)
    # print(result)
    context = {
        "result" : result,
    }
    return render(request, 'app/search.html' , context)