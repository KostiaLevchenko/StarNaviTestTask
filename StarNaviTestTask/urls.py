from django.urls import re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from rest_framework import routers

from knox.views import LogoutView

from apps.user_profile import views as user_profile_views

router = routers.DefaultRouter()
router.register(r'auth-confirm', user_profile_views.AuthConfirm, basename='auth-confirm')


urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    re_path('admin/', admin.site.urls),
    re_path(r'^api/auth/sign-up/', user_profile_views.RegistrationView.as_view(), name='sign-up'),
    re_path(r'^api/auth/sign-in/', user_profile_views.LoginView.as_view(), name='sign-in'),
    re_path(r'^api/auth/logout/', LogoutView.as_view(), name='auth-logout'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
