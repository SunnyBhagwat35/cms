from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.RegisterUser.as_view(), name='user_registration'),
    path('login', views.UserLogin.as_view(), name='user_login'),
    path('create_content', views.CreateContent.as_view(), name="create_content"),
    path('edit_content/<int:pk>', views.EditContent.as_view(), name="edit_content"),
    path('view_content/<int:pk>', views.ViewContent.as_view(), name="view_content"),
    path('delete_content/<int:pk>', views.DeleteContent.as_view(), name="delete_content"),

    path('search_content', views.SearchContent.as_view(), name="search_content"),

    
]