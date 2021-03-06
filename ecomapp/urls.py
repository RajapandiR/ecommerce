from django.urls import path
from ecomapp import views, api
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('check/', views.check, name='check'),
    path('product/<slug>/', views.productView, name='product'),
    path('update-item/', views.updateItem, name='updateItem'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.resetPassword, name='resetPassword'),
    path('forget-password/<uidb64>/<token>', views.forgetPassword, name='forget'),
    # path('shirt/', views.shirt, name='shirt'),
    # path('checkcontinue/', views.checkcontinue, name='checkcontinue'),
    path('history/', views.UserProductHistory, name='history'),
    path('check-success/', views.checkSuccess, name='success'),
    path('order/', views.OrderView, name='order'),
    path('track/<str:pk>/', views.TrackView, name='tracks'),

    # path('api/user', api.UserApiView.as_view()),
    # path('api/category/', api.CategoryApiView.as_view()),
    # path('api/category/<str:pk>/', api.CategoryApi.as_view()),


    # path('reset-password/', auth_views.PasswordResetView.as_view(), name="reset_password"), 
    # path('resetpassword-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('reset<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)