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
import array as arr
import numpy as np

sys.setrecursionlimit(1500)


def home (request):
   
    manga = Manga.objects.filter(category = 1)
    manhua = Manga.objects.filter(category = 2)
    context = {
        'mangaList': manga,
        'manhuaList' : manhua,
    }
    
    return render(request, 'app/home.html', context)


def register (request):
    form = CreateUserForm(request.POST)
    
    # print(request.POST['username'])
    
    
    if('dk' in request.POST):
        if(form.is_valid()):
            print("dk thanh cong")
            form.save()
            messages.info(request, "Đăng ký tài khoản thành công")
        else:
            print("Tài khoản đã tồn tại")
            messages.info(request, "Tài khoản đã tồn tại")
            
    context = {
        'form': form
    }
   
    return render(request, 'app/register.html', context)


def Login (request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == 'POST'):
        if('txtUsername' in request.POST and 'txtPassword' in request.POST):
            username = request.POST['txtUsername']
            password = request.POST['txtPassword']
            print(username)
            print(password)
            user = authenticate(request,username = username , password = password)
            print("user",user)
            
            if user is not None:
                login(request, user)
                print("Mk dùng")
                return redirect('/') 
            else: messages.info(request, "Tk hoac mat khau khong dung")
            

    return render(request, 'app/login.html')


def logoutPage (request):
    logout(request)

    return redirect('/')


def base (request):

    return render(request, 'app/home.html' )


def manga (request, id):
    
    newAvatar = Avatar.objects.all()
    
    image = ""
    
    for item in newAvatar:
                if (item.user.username == request.user.username):
                        avt = item
                        print('admin' , item.image)
                        image = item.image
                        print("avt2" , avt)
                        break
    
    manga = Manga.objects.get(idManga=id)
    
    chapterList = Chapter.objects.filter(idChapter=id)
    
    likedList = MyList.objects.filter(user = request.user , manga = manga)
    
    ratingList = Myrating.objects.filter(user = request.user , manga = manga)
    
    liked = False
    
    ratinged = False
    
    rattingelm = ""
    
    for item in likedList:
        if(item.manga == manga and item.user  == request.user):
           liked = True
           break
    
    for item in ratingList:
        if(item.manga == manga and item.user  == request.user):
           ratinged = True
           rattingelm = item.rating
           break
       
    
    listComment = Comment.objects.filter(manga=id)
    
    tmp  = np.empty(listComment.count(), dtype=object) 
    
    i = 0
    
    for item in listComment:
        for avt in newAvatar:
            if(item.user.username == avt.user.username):
                tmp[i] = avt
                i = i + 1
     
    sum = 0
    
    print("avt array" , tmp)
    
    print('ratting' ,rattingelm)
    
    for item in chapterList:
       sum = sum + item.viewCount
        
    length = chapterList.count()
    
  
    
    context = {
        'manga': manga,
        'chapterList' : chapterList,
        'length' : length,
        'sum' : sum,
        'listComment' : listComment,
        'liked' : liked,
        'ratinged' : ratinged,
        'ratting' : rattingelm,
        'image' : image,
        'imageArray' : tmp,
    }
    
    if(request.method == 'POST'):
        if(request.user.is_authenticated):
            if('ratting' in request.POST): 
                ratting = Myrating(user = request.user , manga = manga , rating = request.POST['ratting'])
                ratting.save()
            
            if('changeratting' in request.POST): 
                ratting = Myrating.objects.get(user = request.user , manga = manga)
                ratting.rating = request.POST['changeratting']
                ratting.save()   
                print("change")
    
            if('comment' in request.POST):
                comment = Comment(user = request.user , manga = manga , context = request.POST['comment'])
                comment.save()
                
            if('like' in request.POST):
                like = MyList(user = request.user , manga = manga )
                like.save()
                
            if('unlike' in request.POST):
                like = MyList.objects.get(user = request.user , manga = manga )
                like.delete()
               
            messages.info(request, "Thao tác thành công")
           
                
        else: 
            messages.info(request, "Bạn cần đăng nhập để sử dụng tính năng này")
           
                    
    return render(request, 'app/manga.html' , context)


def chapter (request,mangaId, chapterId):
    chapter = Chapter.objects.filter(idChapter=mangaId , order = chapterId).first()
    chapterList = Chapter.objects.filter(idChapter=mangaId)
    length = chapterList.count()
    chapter.viewCount = chapter.viewCount + 1
    chapter.save()
    chapterAll = Chapter.objects.filter(idChapter=mangaId)
    print("chapter all" , chapterAll)
    chapterContent = chapter.content
    chapterNext = chapter.order + 1
    chapterPrev = chapter.order - 1
    end = False
    start = False
    
    if(chapterNext > length):
        end = True
        
    if(chapterPrev < 1):
        start = True
        
    # print(chapterNe)
    # print(chapterContent)
    context = {
        'manga': manga,
        'chapterList' : chapter,
        'chapterContent' : chapterContent,
        'chapterAll' : chapterAll,
        'chapterNext' : chapterNext,
        'chapterPrev' : chapterPrev,
        'start' : start,
        'end' : end,
    }

    return render(request, 'app/chapter.html' , context)


def profile (request , username , tabnumber):
    
    newAvatar = Avatar.objects.all()
    
    author = request.user.username == username
    
    user = User.objects.get(username = username)
    
    image = ""
    
    for item in newAvatar:
                if (item.user.username == username):
                        avt = item
                        print('admin' , item.image)
                        image = item.image
                        print("avt2" , avt)
                        break
                    
    
    if(request.method == 'POST'):
            if('username' in request.POST or 'email' in request.POST ):  
                avt.image = request.POST['image']
                avt.save()
                user.username = request.POST['username']
                user.email = request.POST['email']
                user.save()
                messages.info(request, "Cập nhật thông tin thành công")
            
            if('newpassword' in request.POST and 'newpassword2' in request.POST):  
                user.set_password(request.POST['newpassword'])
                user.save()  
                messages.info(request, "Đổi mật khẩu thành công")
             
             
   
    
    print('user', type(user))
    
    likedList = MyList.objects.all()
    
    print("profile" , request.body)
    
    tmp  = np.empty(likedList.count(), dtype=object) 
    
    i = 0
    
    index = 0
         
    for item in likedList:
        if (item.user.username == username):
                tmp[i] = item.manga
                i = i + 1

    
    tmp = list( set(tmp) )
    
    mangaList = np.empty(len(tmp), dtype=object) 
    
          
    for item in tmp:
        if item is not None:
            mangaList[index] = Manga.objects.get(idManga=item)
            print(item)
            index = index + 1
    
    print(image)
    
    context = {
        'user' : user,
        'tabnumber' : tabnumber,
        'mangaList' : mangaList,
        'image' : image,
        'author' : author,
    }
    return render(request, 'app/profile.html' , context)


def hot (request):
    manga = Manga.objects.all().order_by('viewCount')[:5]
    
    print(manga)
    
    context = {
        'mangaList' : manga
    }
    
    return render(request, 'app/hot.html' , context)


def favorite (request):
    likedList = MyList.objects.all()
    
    tmp  = np.empty(likedList.count(), dtype=object) 
    
    i = 0
    
    index = 0
         
    for item in likedList:
        if (item.user == request.user):
                tmp[i] = item.manga
                i = i + 1

    
    tmp = list( set(tmp) )
    
    mangaList = np.empty(len(tmp), dtype=object) 
    
          
    for item in tmp:
        if item is not None:
            mangaList[index] = Manga.objects.get(idManga=item)
            print(item)
            index = index + 1
            
    context = {
        'mangaList' : mangaList
    }
    
    return render(request, 'app/favorite.html' , context)


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
    print("userRating")
    print(userRatings)
    userRatings = userRatings.fillna(0,axis=1)
    print("userRatingcheck")
    print(userRatings)
    corrMatrix = userRatings.corr(method='pearson')
    print("corrMatrix")
    print(corrMatrix)

    user = pd.DataFrame(list(Myrating.objects.filter(user=request.user).values())).drop(['user_id','id'],axis=1)
    print("user")
    print(user)
    user_filtered = [tuple(x) for x in user.values]
    print("user_filtered")
    print(user_filtered)
    movie_id_watched = [each[0] for each in user_filtered]
    print("movie_id_watched")
    print(movie_id_watched)

    similar_movies = pd.DataFrame()
    print("similar_movies")
    print(similar_movies)
    for movie,rating in user_filtered:
        similar_movies = similar_movies.append(get_similar(movie,rating,corrMatrix),ignore_index = True)
    
    print("similar_movies2")
    print(similar_movies)
    
    movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
    print("movies_id")
    print(movies_id)
    movies_id_recommend = [each for each in movies_id if each not in movie_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
    movie_list=list(Manga.objects.filter(idManga__in = movies_id_recommend).order_by(preserved)[:10])
    print("movie_list")
    print(movie_list)
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
    length = len(result)
    
    print("length" , length)
    context = {
        "result" : result,
        "length" : length,
    }
    return render(request, 'app/search.html' , context)