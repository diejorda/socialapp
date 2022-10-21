
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from .tests import idcount

from .models import Follow, Profile, Post, LikePost , Comment
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from itertools import chain, count

from django.http import HttpResponseRedirect, HttpRequest






# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)

    ### user followed, busco perfiles a los que sigue el user loged
    
    users_followed=Follow.objects.filter(loged_id=user_profile.id_user)
    
    usersids=[]
    feed=[]
    feeds=[]
    fof_ids=[]

    fof_profiles=[]
    ## creo una lista con los id de las personas a las que sigue el user loged
    for users in users_followed:
        usersids.append(users.followed_id)
    
    ## con los id busco su objeto profile y filtro en los posts
    
    for ids in usersids:
        #index ,friends post
        profile=Profile.objects.get(id_user=ids)
        
        feed= Post.objects.filter(user=profile)       
        feeds.append(feed)
    
    # index ,friend of friends
        friend_follow_filter=Follow.objects.filter(loged_id=ids)
        for follow in friend_follow_filter:
            fof_ids.append(follow.followed_id)
    
    ids=[]

    # friend of friend that i dont follow.
    for id in usersids:
        fof_ids=[values for values in fof_ids if values != id]
    
    ## Most followed friend of friends
    ids,count=idcount(fof_ids)

    ## friend of friend profiles
    for id in ids:
        fof_profile=Profile.objects.filter(id_user=id)
        fof_profiles.append(fof_profile)
    
        
    fof_profil=list(chain(*fof_profiles))
   

    ### utilizo funcion para que feeds sea renderizable en html
    posts=list(chain(*feeds))

    ## comprimo unformacion en una lista
    fof_data=zip(fof_profil,count)
    fof_data=list(fof_data)
    

    
    return render(request, 'index.html' , {'user_profile':user_profile, 'posts':posts, 'fof_data':fof_data})

@login_required(login_url='signin')
def profile(request, pk):
    loged_user_object=User.objects.get(username=request.user.username)
    loged_user_profile=Profile.objects.get(user=loged_user_object)
    user_obj=User.objects.get(username=pk)
    user=Profile.objects.get(user=user_obj)
    posts=Post.objects.filter(user=user)
    posts_count=posts.count()

    ##Follow-unfollow html
    ## busco en los objetos si existe una instancia que posea los id del user logeado y el user del perfil
    follow_filter=Follow.objects.filter(followed_id=user.id_user , loged_id=loged_user_profile.id_user).first()
    
    if follow_filter == None:
        ## el usuario logeado no sigue al perfil      
        btnfollow = 'Follow'
    else:
        btnfollow = 'Unfollow'

    ## followed count

    follow_count=Follow.objects.filter(followed_id=user.id_user).count()

    ## following count

    following_count=Follow.objects.filter(loged_id=user.id_user).count()
    
    
    context={
        'user_obj': user_obj,
        'user': user,
        'posts':posts,
        'posts_count': posts_count,
        'user_profile': loged_user_profile,
        'btnfollow': btnfollow,
        'follow_count': follow_count,
        'following_count': following_count,


    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def like(request):
    username= request.user.username

    ### post id lo paso por url y creo variable con el objeto buscandolo dentro de los modelos.
    post_id= request.GET.get('post_id')
    post=Post.objects.get(id=post_id)
    ## Busco si existe un objeto like que coincida con el usuario y el post id (filter y first es para que no me de error, sino usaria get)
    
    like_filter= LikePost.objects.filter(username=username,post_id=post_id).first()
    
    # si no existe el objeto que coicida, lo creo y aumento los like del post
    if like_filter == None:
        new_like=LikePost.objects.create(username=username,post_id=post_id)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        
        return redirect('/')
    else:
        ## si existe borro el objeto y reduzco los like del post. 
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    user_followed_id=int(request.GET.get('userid'))
    user_followed_object=Profile.objects.get(id_user=request.GET.get('userid'))
    user_followed_username=user_followed_object.user.username
    loged_user_object=User.objects.get(username=request.user.username)
    loged_user_profile=Profile.objects.get(user=loged_user_object)
    user_loged_id=int(loged_user_profile.id_user)

    page=request.GET.get('page')
    

    follow_filter=Follow.objects.filter(followed_id=user_followed_id,loged_id=user_loged_id).first()
    
    if follow_filter == None:
        ## no se estan siguiendo
        follow_instance=Follow.objects.create(followed_id=user_followed_id,loged_id=user_loged_id)
        follow_instance.save()
        if page == 'profile':
            return redirect('profile', user_followed_username)
       
        else: 
            return redirect('index')
        

    else:## se siguien
        follow_filter.delete()
        if page == 'profile':
            return redirect('profile', user_followed_username)
        else: 
            return redirect('index')

@login_required(login_url='signin')            
def search(request):
    ##---- User Profile
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    ##-------Search 
    users=[]
    profiles=[]
    btnfollows=[]
    if request.method== 'POST':
        search_parameter=request.POST['username']
        users=User.objects.filter(username__icontains=search_parameter)
        for user in users:
            profile=Profile.objects.filter(user=user).first()
            profiles.append(profile)
    
    
        
        

    return render(request , 'search.html',{'profiles': profiles, 'user_profile':user_profile})
    




def signup(request):
### CONTROL DE SIGN UP--------------------------## agregar usuarios (import authmodels import User, auth)
    if request.method == 'POST':
        username = request.POST['username'] ## llamo al value del form en el elemento username llamandolo por el atributo name del html
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        ## checkeos de pwd y singluaridad de mail y username-----------------------------

        if password == password2: ## importo messages de contrib para mandar errores al frontend
            if User.objects.filter(email=email).exists(): ## si el elemento eemail de User.objects existe
                messages.info(request, 'email taken') ## deben ser llamados desde el html
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            
            else: ## ALL CHECK
                user = User.objects.create_user(username=username, email=email, password=password) ## metodo del objeto User
                user.save() 
                ### Por el momento solo tengo resuelto la creada del usuario pero debo linkear con la creacion de un profile para el mismo
                ### log user in and redirct to settings page.
                user_login= auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                ## create a profile object for the new user--------------
                ## uso objects.get por que necesito pasarle el objeto al modelo Profile
                ## en parametro de busqueda utilizo username, podria usar el email tambien
                user_model= User.objects.get(username=username)
                ## creo una instancia de Profile y le paso los atributos requeridos, que son el objeto usermodel y su id.
                new_profile= Profile.objects.create(user=user_model,id_user=user_model.id) ## el resto puede ser blank
                new_profile.save()
                ## retorno a login 
                return redirect('settings')
        else:
            messages.info(request,'Passwords Do Not Match')
            return redirect('signup')
    
    #### request GET -------------------------    
    else:
        return render(request, 'signup.html', {} )
    
def signin(request):
    ## log in method post
    if request.method == 'POST':
        username= request.POST['username']
        password=request.POST['password']
        
        user = auth.authenticate(username=username, password=password)


        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            
            messages.info(request, 'Nombre de usuario o contraseña no son correctos')
            return redirect('signin')

        

    else: return render(request, 'signin.html', {})

def logout(request):

    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_model=auth.get_user(request)
    
    user_profile=Profile.objects.get(user=request.user)


    if request.method == 'POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        
        aboutme=request.POST['aboutme']
        relationship=request.POST['relationship']
        workingat=request.POST['workingat']
        location=request.POST['location']

        if request.FILES.get('image') == None:
            image=user_profile.profileimg
        else:
            image=request.FILES.get('image')

        user_profile.first_name=firstname
        user_profile.last_name=lastname
        user_profile.aboutme=aboutme
        user_profile.workingat=workingat
        user_profile.location=location
        user_profile.relationship=relationship
        user_profile.profileimg=image

        user_profile.save()
        
        return redirect('settings')
        
        

    else: return render(request,'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def post(request):
    
    if request.method == 'POST':
         image=request.FILES.get('image')
         caption=request.POST['caption']
         location= request.POST['location']
         user_profile=Profile.objects.get(user=request.user)

         new_post=Post.objects.create(user=user_profile, image=image ,caption=caption , location=location)
         new_post.save()
         return redirect('index')
         
    
    
    else:
        return render(request,'post.html', {})

@login_required(login_url='signin')
def comment(request):
    ###Form
    comment=request.POST['comment']
   
    
    if comment== None:
        return redirect('/')
    
    else:
        ##Loged profile
        user_object=User.objects.get(username=request.user.username)
        user_profile=Profile.objects.get(user=user_object)

        ## Create comment
        p_id=request.POST['post']
        post=Post.objects.filter(id=p_id).first()
        new_comment=Comment.objects.create(user_commenting=user_profile,post=post, text=comment)
        new_comment.save()
        
        return redirect('/')
    