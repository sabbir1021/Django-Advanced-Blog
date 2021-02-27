from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('', views.PostView.as_view(), name='post_list'),
    path('<int:pk>/<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetailView.as_view(), name='post_detail'),
]