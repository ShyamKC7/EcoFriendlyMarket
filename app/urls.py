from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.ProductView.as_view(), name="home"), 
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
     name='password_reset'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('greengadgets/', views.greengadgets, name='greengadgets'),
    path('greengadgets/<slug:data>', views.greengadgets, name='greengadgetsdata'),
    path('accounts/login/', auth_views.LoginView.as_view (template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('registration/', views.CustomerRegistrationView.
    as_view(), name="customerregistration")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
