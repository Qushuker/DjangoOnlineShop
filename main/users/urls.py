from django.urls import path
from .views import register, login_view, CustomPasswordChangeView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from .views import ProfileView, edit_profile


urlpatterns = [
    path('signup/', register, name='signup'),
    path('signin/', login_view, name='signin'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]