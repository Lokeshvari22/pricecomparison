from django.contrib import admin
from django.urls import path
from home import views
from django.contrib.auth.models import User,auth
urlpatterns = [
    path('',views.index,name="home"),
    path('login',views.login,name="login"),
    path('register',views.register,name='register'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('search',views.search,name='search'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('smartwatch',views.smartwatch,name='smartwatch'),
    path('camera',views.camera,name='camera'),
    path('headphone',views.headphone,name='headphone'),
    path('television',views.television,name='television'),
    path('speaker',views.speaker,name='speaker'),
    path('offspeaker',views.offspeaker,name='offspeaker'),
    path('offsmartwatch',views.offsmartwatch,name='offsmartwatch'),
    path('offheadphone',views.offheadphone,name='offheadphone'),
    path('compare', views.compare, name='compare'),  # ✅ New compare route
    path('products',views.products,name='products')
    # path('profile_update',views.profile_update,name='profile_update')
]