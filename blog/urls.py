from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archives'),
    path('category/<int:category_id>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:tag_id>/', views.TagView.as_view(), name='tag')
    ]