from .import views
from django.urls import path
from django.urls import include
from knox import views as knox_views
from userauth.views import login_api
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    #user auth
    path('api/authenticate', login_api, name='login'),
    path('logout', knox_views.LogoutView.as_view()),
     path('logoutall',knox_views.LogoutAllView.as_view()),
   
   #user registration
    path('api/register',views.register),
    path('api/driverRegister', views.driverRegister),

    #user request endpoints
    path('api/request', views.user_request),
    path('api/mytrips', views.my_trips, name='my_trips'),


    #driver requesr endpoints
    path('api/available_requests', views.available_requests),
    path('api/available_requests/<int:request_id>', views.request_detail),
    path('api/accept_request', views.accepted_requests),
    path('api/complete_trip', views.complete_trip),
    path("api/drivertrips", views.drivertrips),

    #password reset urls
    path('api/password_reset', csrf_exempt(auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html')), name='password_reset'),
    path('api/password_reset/done', csrf_exempt(auth_views.PasswordResetDoneView.as_view(template_name ='accounts/password_reset_sent.html')), name='password_reset_done'),
    path('api/reset/<uidb64>/<token>', csrf_exempt(auth_views.PasswordResetConfirmView.as_view(template_name ='accounts/password_reset_form.html')), name='password_reset_confirm'),
    path('api/reset/done', csrf_exempt(auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html')), name='password_reset_complete'),

#daraja API
    path('api/payment',views.payment),
    path('api/payment-result',views.payment_results)


]
