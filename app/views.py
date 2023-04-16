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

sys.setrecursionlimit(1500)


def home (request):
    form = CreateUserForm()
    manga = Manga.objects.filter(category = 'Action - Comedy - Manga')
    manhua = Manga.objects.filter(category = 'Adventure - Manhua - Truyện Màu')
    context = {
        'mangaList': manga,
        'manhuaList' : manhua,
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
        }
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



def category (request):
  
    return render(request, 'app/category.html')




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