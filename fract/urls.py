from django.urls import path
from .views import ImageListView, ImageDetailView, LikedImageListView
from . import views
from users import views as user_views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', ImageListView.as_view(), name='index'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image'),
    path('add_like/<int:img_id>/', user_views.add_like, name='add_like'),
    path('likes', LikedImageListView.as_view(), name='likes'),
    path('about/', views.about, name='about'),
    path('images_filtered/', views.images_filtered, name='images_filtered'),        
]   