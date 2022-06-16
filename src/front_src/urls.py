from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import home_page
from .blog import blog_index
urlpatterns = [
    	path('', home_page, name='home_page'),
        path('blog/', blog_index, name='bog_index'),
]

