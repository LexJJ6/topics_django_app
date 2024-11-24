from django.urls import path
from . import views

# isto já localhost:8000/topics/

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_topic, name="new_topic"), # o name nao tinha de ser igual ao nome da funcao em views.py mas assim fica mais facil
    path("<int:topic_id>/", views.topic_details, name="topic_details"),
    path("<int:topic_id>/edit/", views.edit_topic, name="edit_topic"),
    path("<int:topic_id>/delete/", views.delete_topic, name="delete_topic"),
    path("<int:topic_id>/new-comment/", views.new_comment, name="new_comment"),
    path("<int:topic_id>/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path("<int:topic_id>/<int:comment_id>/delete/", views.delete_comment, name="delete_comment")
]