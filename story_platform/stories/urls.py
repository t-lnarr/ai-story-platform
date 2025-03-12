from django.urls import path
from . import views

urlpatterns = [
    path("", views.story_list, name="story_list"),
    path("story/<int:story_id>/", views.story_detail, name="story_detail"),
    path("new/", views.new_story, name="new_story"),
    path("story/<int:story_id>/comment/", views.add_comment, name="add_comment"),
    path("story/<int:story_id>/like/", views.add_like, name="add_like"),
    path("register/", views.register, name="register"),
    

]
