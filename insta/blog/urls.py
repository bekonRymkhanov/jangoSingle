
from django.urls import path,include
from blog import views

urlpatterns = [
    path('listBlogs/',views.listOfPosts,name="list_of_posts"),
    path('listBlogs/details/<int:id>/', views.postDetails, name='details'),

    path('deletePost/<int:id>/', views.delete_post, name="delete_post"),
    path('editPost/<int:id>/', views.editPost, name="edit_post"), 


    path('createComment/<int:id>/', views.addComment, name="create_comment"), 

]