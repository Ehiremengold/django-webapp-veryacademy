from django.urls import path
from .views import index, LikeView, search, create, update, delete, detail, post_by_category, needskill
from django.conf.urls import url

urlpatterns = [
    path('', index, name="index"),
    path('I-need/what-services/', needskill, name="needskill"),
    path('share-hustle/create-new/', create, name="create"),
    path("<str:slug>/edit/", update, name="update"),
    path("<str:slug>/delete/", delete, name="delete"),
    path("more/<str:slug>/", detail, name="details"),
    path("q/search/", search, name="search"),
    path('category/<str:category_slug>/', post_by_category, name="post_by_category"),
]

