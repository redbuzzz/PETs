from django.urls import path, include

from authorization.views import ActivateAccountView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('activate/<str:uid>/<str:token>', ActivateAccountView.as_view())]