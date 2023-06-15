from .import views
from django.urls import path
from django.urls import include
from knox import views as knox_views
from userauth.views import login_api

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

    #driver requesr endpoints
    path('api/available_requests', views.available_requests),
    path('api/available_requests/<int:request_id>', views.request_detail),
    path('api/accepted_requests', views.accepted_requests),
    path('api/complete_trip', views.complete_trip),




]
