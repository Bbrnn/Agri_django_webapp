"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from  products import views


urlpatterns = [
    path('register/', views.user_register, name='user_register'),

    path('login/', views.user_login, name='login'),

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product_list/', views.product_list, name='product_list'),

    path('contact/', views.contact_view, name='contact'),
    #path('contact/success/', views.contact_success, name='contact_success'),
    path('admin/', admin.site.urls),

    path('<int:product_id>/', views.product_detail, name='product_detail'),
    #path('create/', views.product_create, name='product_create'),
    #path('<int:product_id>/update/', views.product_update, name='product_update'),
    #path('<int:product_id>/delete/', views.product_delete, name='product_delete'),


]



# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)