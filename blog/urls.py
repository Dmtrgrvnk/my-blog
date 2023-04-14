from django.urls import path

from . import views


app_name = 'blog'  # application namespace


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    # path to sent e-mail template
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
]
