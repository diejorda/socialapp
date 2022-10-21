from distutils.command.upload import upload
from email.policy import default
from time import timezone
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
import uuid ## create unique id.
from datetime import date


# Create your models here
# creacion de modelo de perfil, (profile picture, bio, location, etc)
## auth user model only gives fields for username, first name , last name email and password, but we need to add more fields.
## we can create a custom user model and link it to user model using a foreign key

User= get_user_model()

class Profile(models.Model):
    ## para user queremos likear el profile con usermodel usando una forein key, DE esta manera obtendremos el usuario que esta logeado
    ## tengo que importar de auth get_user_model
    
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    id_user= models.IntegerField()

    first_name=models.CharField(max_length=20, blank=True)
    last_name=models.CharField(max_length=20, blank=True)
    aboutme = models.TextField(default='bio')
     ## hay que crear models en settings y agregar en urls.py las roots para las media
    ## a su vez hay que crear la carpeta porfile_images para guardar las imagenes que los usuarios coloquen en su perfil
    ## tambien le vamos a dar una profile pic por defecto guardada en carpeta media media
    profileimg=models.ImageField(upload_to='profile_images', default='blank-profile-pic.png')
    location=models.CharField(max_length=100, blank=True)
    relationship=models.CharField(max_length=20, blank=True)
    workingat=models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.user.username ## username por que si pongo user me va a mostrar el objeto y lo que busco es que retorne el elemento username del objeto.


### por ultimo debo permitir el acceso al modelo desde el panel de admin, desde admin.py

class Post(models.Model):
    ## se convierte en el id de la instancia, reemplaza el id clasico.
    id=models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    

    image=models.ImageField(upload_to='post_images')
    caption=models.TextField(blank=True)
    created_at=models.DateTimeField(default=date.today())
    no_of_likes=models.IntegerField(default=0)
    location=models.CharField(blank=True, max_length=40)
    
    

    def __str__(self):
        strid=str(self.id)
        return strid

class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username= models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Follow(models.Model):
    followed_id=models.CharField(max_length=100, default=1)
    loged_id= models.CharField(max_length=100, default=1)

    def __str__(self):
        return self.followed_id

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    text=models.CharField(max_length=255)
    user_commenting=models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_commenting.user.username
    