
from django.urls import path
from  . import views

from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('buy/', views.buy, name='buy'),

]
