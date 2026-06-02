"""
URL configuration for shoppinglyx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductView, Productdetails, customerregistration, ProfileView, EmailLoginView
from django.contrib.auth import views as auth_views
from .forms import MypasswordChangeForm, MypasswordResetForm, MysetpasswordForm
from django.urls import reverse_lazy

urlpatterns = [
                  # path('', views.home),
                  path('', ProductView.as_view(), name='ptoductview'),
                  # path('product-detail/', views.product_detail, name='product-detail'),
                  path('product-detail/<int:pk>', Productdetails.as_view(), name='product-detail'),
                  path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
                  path('cart', RedirectView.as_view(pattern_name='showcart', permanent=False)),
                  path('cart/', views.show_cart, name='showcart'),

                  # path('pluscart/', views.plus_cart, name='pluscart'),
                  # path('minuscart/', views.minus_cart, name='minuscart'),
                  # path('removecart/', views.remove_cart, name='removecart'),
                  path('pluscart/', views.plus_cart, name='pluscart'),
                  path('minuscart/', views.minus_cart, name='minuscart'),
                  path('removecart/', views.remove_cart, name='removecart'),

                  path('buy/', views.buy_now, name='buy-now'),
                  path('profile/', ProfileView.as_view(), name='profile'),
                  path('address/', views.address, name='address'),

                  path('orders/', views.orders, name='orders'),

                  path('search/', views.search, name='search'),

                  # path('changepassword/', views.change_password, name='changepassword'),
                  path('mobile/', views.mobile, name='mobile'),
                  path('topwear/', views.topwear, name='topwear'),
                  path('bottomwear/', views.bottomwear, name='bottomwear'),
                  # path('mobile/<slug:data>', views.mobile, name='mobile'),
                  path('laptop/', views.laptop, name='laptop'),

                  path('accounts/login/', EmailLoginView.as_view(), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

                  # path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class = MypasswordChangeForm , success_url='/passwordchangedone'),name ='passwordchange') ,
                  # path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

                  path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
                                                                                form_class=MypasswordChangeForm,
                                                                                success_url=reverse_lazy(
                                                                                    'passwordchangedone')),
                       name='passwordchange'),
                  path('passwordchangedone/',
                       auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),
                       name='passwordchangedone'),

                  path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
                                                                               form_class=MypasswordResetForm),
                       name='password_reset'),
                  path('password-reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
                       name='password_reset_done'),
                  path('password-reset/donfirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
                                                                   form_class=MysetpasswordForm),
                       name='password_reset_confirm'),
                  path('password-reset-complete/',
                       auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
                       name='password_reset_complete'),

                  path('registration/', customerregistration.as_view(), name='customerregistration'),
                  path('checkout/', views.checkout, name='checkout'),
                  path('checkout/', views.checkout, name='checkout'),
                  path('paymentdone/', views.payment_done, name='paymentdone'),
                  path('success/', views.payment_success, name='payment_success'),
                  path('cancel/', views.payment_cancel, name='payment_cancel'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
